#!/usr/bin/python

# observant_agent

from .agent_config import *
from .gamestate import StateModule
from .tracker import scan
from .map import checkPath, proceed
from .utilities import *
from .reader import read
from .time import countStep
from .combatTactics import meleeCombat
from .doctor import checkup, fixMinorProblems, fixUrgentProblems
from .inventory import checkUnderfoot, nabGoodies

agenda = [] # populated at EOF (so all the functions are defined first)
messages = []
stepsSinceLastAction = [0]
def chooseAction(state, observations):
	for protocol in agenda:
		action = protocol(state,observations)
		if type(action) != int:
			# This is a fatal error, so we print even if CONST_QUIET
			if action == None:
				print("\x1b[0;31mFatal error: Protocol didn't return anything.")
				print("Protocol at fault: ",end="")
				print(protocol)
				exit(1)
			if type(action) == tuple:
				print("\x1b[0;31mFatal error: Protocol returned a tuple.")
				print("Protocol at fault: ",end="")
				print(protocol)
				exit(1)
			if type(action) == list:
				print("\x1b[0;31mFatal error: Protocol returned a list.")
				print("Protocol at fault: ",end="")
				print(protocol)
				exit(1)
			print("\x1b[0;31mFatal error: Protocol returned unexpected type. (",end="")
			print(type(action),end=")\n")
			print("Protocol at fault: ",end="")
			print(protocol)
			exit(1)
		if action != -1:
			return action
	state.dumpCore("Agent has panicked! (Its logic gives it no move to make.)",observations)
	state.get("queue").append("y")
	return 65 # Quit, then next step, answer yes to "are you sure?"

class ActionQueue(StateModule):
	def __init__(self, state):
		self.queue = []
		self.state = state
	def reset(self):
		self.queue = []
	def dumpCore(self):
		if len(self.queue) == 0:
			return
		if len(self.queue) == 1:
			print("Agent was just about to press ",end="")
			print(self.queue[0],end=".\n")
		else:
			print("Agent had intended to take the following actions: ",end="")
			print(self.queue)
			
	def displayStats(self):
		pass
	def append(self, item):
		if type(item) == list:
			for x in item:
				self.queue.append(x)
		else:
			if type(item) == str:
				for x in item:
					self.queue.append(keyLookup[x])
			else:
				self.queue.append(item)
	def pop(self, observations):
		if len(self.queue) == 0:
			return -1
		item = self.queue[0]
		self.queue = self.queue[1:]
		if isinstance(item, bool):
			# Bools in the queue signify the following:
			# "There may or may not be a y/n question at this point.
			# If there is, respond with {y/n}. Otherwise, just proceed."
			# True indicates "respond with y", and false indicates "respond with n".
			msg = readMessage(observations)
			if msg.find("[yn") != -1:
				if item == True:
					return 7 # y
				else:
					return 5 # n
			else:
				# no y/n question detected; proceed to next element in queue
				return self.pop(observations)
		return item
	def cutInLine(self,item):
		# Shove this action to the front of the queue
		# Useful in emergencies when we can't afford to wait
		self.queue = [item] + self.queue

def handleQueue(state, observations):
	# Careful! No observations are recorded until the queue is empty.
	# If that causes problems for you, don't use the queue.
	return state.get("queue").pop(observations)

def recordingDone(state, observations):
	state.get("tracker").returnToTop()
	state.get("map").returnToTop()
	state.get("reader").returnToTop()
	state.get("inventory").returnToTop()
	state.get("time").updateTurns(readTurn(observations))
	#state.get("time").incrementTurns()
	stepsSinceLastAction[0] = 0
	return -1

def advancePrompts(state, observations):
	if observations["misc"][0]:
		return 7 # y/n prompt, just hit y
	if observations["misc"][1] or observations["misc"][2]:
		return 19 # Game waiting for enter, so hit enter
	return -1

agenda = [
	countStep,
	read,
	handleQueue,
	checkup,
	scan,
	checkPath,
	checkUnderfoot,
	# Check the engraving underfoot, verify whether or not you're standing on an ELBERETH
	# ...Actually, maybe check for "closed for inventory" and "ad aerarium" too, come to think of it
	advancePrompts,
	
	# Nothing above this point in the agenda is supposed to do anything that spends a turn.
	recordingDone,
	# Nothing below this point in the agenda is supposed to do anything that doesn't spend a turn.
	
	fixUrgentProblems,
	# drop your gold if a guard instructs you to; antagonizing a guard tends to be YASD
	# Consider using escape items if needed
	# Pray if you're otherwise f'd
	meleeCombat,
	# Ranged combat
	nabGoodies,
	fixMinorProblems,
	proceed
]