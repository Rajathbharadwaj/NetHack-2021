#!/usr/bin/python

from .names import monsterNames
from .gamestate import StateModule
from .utilities import *
import random

class LogbookEntry(object):
	def __init__(self):
		self.pos = [] # row, then col
		self.glyph = -1
		self.turnLastSeen = -1
		self.hostility = 1 # 1 = hostile, 0 = peaceful, -1 = tame; maybe we can even use this to track tameness value
	def updatePos(self, pos, turn):
		self.pos = pos
		self.turnLastSeen = turn

class MonsterTracker(StateModule):
	agenda = []
	def __init__(self, state):
		self.names = monsterNames
		random.shuffle(self.names) # variety is the spice of life
		self.lookup = {}
		self.database = []
		for x in range(len(self.names)):
			self.lookup[self.names[x]] = x
			self.database.append(LogbookEntry())
		self.phase = 0
		self.nextOpenName = 0
		self.toName = []
		self.state = state
	def reset(self):
		if not CONST_QUIET:
			print(self.nextOpenName,"names assigned to monsters.")
		random.shuffle(self.names)
		self.database = []
		for x in range(len(self.names)):
			self.lookup[self.names[x]] = x
			self.database.append(LogbookEntry())
		self.phase = 0
		self.nextOpenName = 0
		self.toName = []
	def dumpCore(self):
		pass
	def update(self, observations):
		return self.agenda[self.phase](self,observations)
	
	def look(self, observations):	
		if observations["misc"][2]:
			return -1 # wait for the dialogue box to be dismissed
		self.phase += 1
		self.state.get("queue").append(55) # "What do you want to look at?" -> All monsters on map
		return 93 # whatis
	def readScreen(self, observations):
		if parse(observations["tty_chars"][0])[:12] != "All monsters":
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
				if name == "Agent":
					continue
				try:
					nameIndex = self.lookup[name]
				except KeyError:
					needsName = True
			
			comma = string.find(",")
			col = int(string[open+1:comma])-1
			row = int(string[comma+1:close])
			if needsName:
				#print("Named:",string)
				self.toName.append([row,col])
			else:
				self.database[nameIndex].updatePos([row,col], turn)
		return 19 # next page, please
	def christenNewFaces(self, observations):
		while len(self.toName) > 0 and self.state.get("map").readSquare(observations,self.toName[0][0],self.toName[0][1]) == 267:
			self.toName = self.toName[1:] # Don't try to name shopkeepers, it doesn't work
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
		self.database[self.lookup[name]].updatePos(targetPos, readTurn(observations))
		name += "\n" # Queue up an enter key press to complete the naming process
		self.state.get("queue").append(name)
		self.phase -= 1
		self.toName = self.toName[1:]
		return 18 # "." – tells the game we're ready to name the thing on this square
	def returnToTop(self):
		self.phase = 0
	agenda = [
		look,
		readScreen,
		christenNewFaces,
		moveCursor
	]
	def getNewName(self):
		self.nextOpenName += 1
		try:
			return self.names[self.nextOpenName-1]
		except IndexError:
			print("Fatal error: We're out of names! Please add more to names.py.")
			exit(1)

def scan(state,observations):
	action = state.get("tracker").update(observations)
	return action