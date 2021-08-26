#!/usr/bin/python

from .names import monsterNames, reservedNames
from .gamestate import StateModule
from .utilities import *
import random

class LogbookEntry(object):
	def __init__(self):
		self.pos = [] # row, then col
		self.glyph = -1
		self.turnLastSeen = -1
		self.hostility = 1 # 1 = hostile, 0 = peaceful, -1 = tame; maybe we can even use this to track tameness value
	def updatePos(self, pos, observations):
		self.pos = pos
		self.turnLastSeen = readTurn(observations)
	def setGlyph(self, glyph):
		realGlyph = glyph
		if realGlyph >= 381 and realGlyph < 762:
			# This is a pet, so we'll subtract 381 to see what kind of monster it actually is
			# And also mark it as a pet
			realGlyph -= 381
			self.hostility = -1
		self.glyph = realGlyph

class MonsterTracker(StateModule):
	agenda = []
	def __init__(self, state):
		self.names = monsterNames.copy()
		random.shuffle(self.names) # variety is the spice of life
		self.names += reservedNames
		self.lookup = {}
		self.database = []
		for x in range(len(self.names)):
			self.lookup[self.names[x]] = x
			self.database.append(LogbookEntry())
		self.phase = 0
		self.nextOpenName = 0
		self.toName = []
		self.stances = [] # parallel array to toName; note whether a newly-spotted monster is hostile
		self.state = state
		self.visibleMonsters = {}
	def reset(self):
		if not CONST_QUIET:
			print(self.nextOpenName,"names assigned to monsters.")
			print(len(self.visibleMonsters),"monsters visible when the agent died.")
		self.names = self.names[:len(monsterNames)]
		random.shuffle(self.names)
		self.names += reservedNames
		self.database = []
		for x in range(len(self.names)):
			self.lookup[self.names[x]] = x
			self.database.append(LogbookEntry())
		self.phase = 0
		self.nextOpenName = 0
		self.toName = [] 
		self.stances = []
		self.visibleMonsters = {}
	def dumpCore(self):
		pass
	def update(self, observations):
		return self.agenda[self.phase](self,observations)
	
	def look(self, observations):	
		if observations["misc"][0] or observations["misc"][1] or observations["misc"][2]:
			return -1 # wait for the dialogue box to be dismissed
		self.visibleMonsters = {}
		self.phase += 1
		self.state.get("queue").append(55) # "What do you want to look at?" -> All monsters on map
		return 93 # whatis
	def readScreen(self, observations):
		if parse(observations["tty_chars"][23])[:8] != "--More--":
			self.phase += 1
			return self.agenda[self.phase](self,observations)
		turn = readTurn(observations)
		for x in range(len(observations["tty_chars"])):
			string = parse(observations["tty_chars"][x])
			open = string.find("<")
			if(open == -1):
				continue
			close = string.find(">")
			if string[close+3] == "I":
				continue # Don't bother trying to name something you can't see
			desc = string[close+6:]
			
			calledIndex = desc.find(" called ")
			
			needsName = False
			if calledIndex == -1:
				needsName = True
			else:
				name = desc[calledIndex+len(" called "):]
				end = name.find(" ")
				name = name[:end]
				if name[-1] == ",":
					name = name[:-1] # snip commas off the end, they're not part of the name
				try:
					nameIndex = self.lookup[name]
				except KeyError:
					needsName = True
			
			comma = string.find(",")
			col = int(string[open+1:comma])-1
			row = int(string[comma+1:close])
			
			if (row, col) == (readHeroPos(observations)):
				# No need to assign ourselves a database slot – 
				# we track our own condition quite closely already, tyvm.
				# Previously, I detected this case by the agent's name.
				# Turns out, though, sometimes a spawned ghost will have your name.
				# In that situation, we DO want to give the ghost a name.
				# So we'll detect the "it's us" case this way instead.
				continue
			if observations["glyphs"][row][col] == 267:
				# We can't name shopkeepers. 
				# Fortunately, they do actually have unique names already.
				i = -1
				for x in range(len(desc)):
					if desc[x].isupper():
						i = x
						break
				if i == -1:
					print("Error code 6996 – shopkeeper name handling in tracker.py failed miserably")
					exit(1)
				name = desc[i:]
				commaIndex = name.find(",")
				if commaIndex != -1:
					name = name[:commaIndex]
				else:
					titleIndex = name.find(" the ")
					if titleIndex != -1:
						name = name[:titleIndex]
					else:
						end = name.find("  ")
						name = name[:end]
				# We don't try-catch this like we did for the lookup before
				# if we don't have an entry for this name we need to let the exception fall through
				# We can't change the shopkeeper's name to match our names,
				# so it had BETTER exist in our names somewhere already...
				nameIndex = self.lookup[name]
				needsName = False
				
			
			tameIndex = desc.find("tame")
			peaceIndex = desc.find("peaceful")
			stance = 1
			if peaceIndex != -1:
				stance = 0
			if tameIndex != -1:
				stance = -1
			
			if needsName:
				#print("Named:",string)
				self.toName.append([row,col])
				self.stances.append(stance)
			else:
				self.database[nameIndex].updatePos([row,col], observations)
				self.database[nameIndex].hostility = stance
				self.visibleMonsters[row,col] = self.database[nameIndex]
		if len(self.toName) >= 10 and not CONST_QUIET:
			print("Whoawhoawhoa, that's a lot of new monsters. (",end="")
			print(len(self.toName),end=")\n")
		return 19 # next page, please
	def jotDownGlyphs(self, observations):
		for x in self.visibleMonsters:
			mon = self.visibleMonsters[x]
			row, col = mon.pos
			glyph = observations["glyphs"][row][col]
			mon.setGlyph(glyph)
		self.phase += 1
		return self.update(observations)
	def christenNewFaces(self, observations):
		if len(self.toName) == 0:
			return -1 # Naming complete, let's move on
		self.phase += 1
		self.state.get("queue").append(54) # "What do you want to name?" -> A monster
		return 27
	def moveCursor(self, observations):
		cursorPos = readCursorPos(observations)
		targetPos = self.toName[0]
		# Move cursor to the coordinates of targetPos
		if cursorPos[0] > targetPos[0]:
			return 0
		if cursorPos[0] < targetPos[0]:
			return 2
		if cursorPos[1] > targetPos[1]:
			return 3
		if cursorPos[1] < targetPos[1]:
			return 1
		# Cursor in correct place; input name
		name = self.getNewName()
		self.database[self.lookup[name]].hostility = self.stances[0]
		self.database[self.lookup[name]].updatePos(targetPos, observations)
		self.database[self.lookup[name]].setGlyph(observations["glyphs"][targetPos[0]][targetPos[1]])
		self.visibleMonsters[targetPos[0],targetPos[1]] = self.database[self.lookup[name]]
		name += "\n" # Queue up an enter key press to complete the naming process
		self.state.get("queue").append(name)
		self.phase -= 1
		self.toName = self.toName[1:]
		self.stances = self.stances[1:]
		return 18 # "." – tells the game we're ready to name the thing on this square
	def returnToTop(self):
		self.phase = 0
	agenda = [
		look,
		readScreen,
		jotDownGlyphs,
		christenNewFaces,
		moveCursor
	]
	def getNewName(self):
		self.nextOpenName += 1
		if self.nextOpenName < len(monsterNames):
			return self.names[self.nextOpenName-1]
		else:
			# We could try to dip into the reserved names to survive, I guess
			# But I'd just as soon fail transparently
			print("Fatal error: We're out of names! Please add more to names.py.")
			exit(1)
	def tattle(self, row, col):
		# Named for the skill in Paper Mario 64 and Paper Mario: The Thousand Year Door
		# You point to a monster and ask for more information about it
		# In this case, we fetch its database entry if possible
		try:
			mon = self.visibleMonsters[row,col]
		except KeyError:
			# No database entry found.
			# Maybe whatever called this function pointed to a square with no monster.
			# Maybe the monster is something we can't log in the database.
			# Whatever the reason, we return None to signal "too bad, no information available."
			return None
		else:
			return mon

def scan(state,observations):
	action = state.get("tracker").update(observations)
	return action