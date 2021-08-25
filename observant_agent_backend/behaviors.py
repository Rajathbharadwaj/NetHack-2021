#!/usr/bin/python

# observant_agent

from .agent_config import *
from .gamestate import StateModule
from .tracker import scan
from .map import checkPath, proceed
from .utilities import *
from .reader import read
from .time import countStep

agenda = [] # populated at EOF (so all the functions are defined first)
messages = []
stepsSinceLastAction = [0]
def chooseAction(state, observations):
	for protocol in agenda:
		action = protocol(state,observations)
		if type(action) != int:
			# This is a fatal error, so we print even if CONST_QUIET
			if action == None:
				print("Fatal error: Protocol didn't return anything.")
				print("Protocol at fault: ",end="")
				print(protocol)
				exit(1)
			if type(action) == tuple:
				print("Fatal error: Protocol returned a tuple.")
				print("Protocol at fault: ",end="")
				print(protocol)
				exit(1)
			if type(action) == list:
				print("Fatal error: Protocol returned a list.")
				print("Protocol at fault: ",end="")
				print(protocol)
				exit(1)
			print("Fatal error: Protocol returned unexpected type. (",end="")
			print(type(action),end=")\n")
			print("Protocol at fault: ",end="")
			print(protocol)
			exit(1)
		if action != -1:
			return action
	state.dumpCore("Agent has panicked! (Its logic gives it no move to make.)",observations)
	state.get("queue").append(7)
	return 65 # Quit, then next step, answer yes to "are you sure?"

class ActionQueue(StateModule):
	def __init__(self):
		self.queue = []
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
	def pop(self):
		if len(self.queue) == 0:
			return -1
		item = self.queue[0]
		self.queue = self.queue[1:]
		return item
	def cutInLine(self,item):
		# Shove this action to the front of the queue
		# Useful in emergencies when we can't afford to wait
		self.queue = [item] + self.queue

def handleQueue(state, observations):
	# Careful! No observations are recorded until the queue is empty.
	# If that causes problems for you, don't use the queue.
	return state.get("queue").pop()

def recordingDone(state, observations):
	state.get("tracker").returnToTop()
	state.get("map").returnToTop()
	state.get("reader").returnToTop()
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
	scan,
	checkPath,
	# Check the engraving underfoot, verify whether or not you're standing on an ELBERETH
	# Fight fight fight fight fight
	# Fud
	advancePrompts,
	recordingDone,
	proceed
]

# Get info on monsters: 93-54