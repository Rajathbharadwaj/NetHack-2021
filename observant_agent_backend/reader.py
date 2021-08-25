#!/usr/bin/python

from .gamestate import StateModule
from .agent_config import *
from .utilities import *

class MessageSecretary(StateModule):
	def __init__(self, state):
		self.log = []
		self.state = state
		self.phase = 0
	def reset(self): 
		if not CONST_QUIET:
			if len(self.log) == 0:
				print("Fate unclear. (No messages)")
			else:
				print("Fate: " + self.log[-1][0])
		self.log = []
		self.phase = 0
	def dumpCore(self):
		print("Recent messages:")
		for string, streak in self.log[-10:]:
			if streak > 1:
				print("\t"+string+" ("+str(streak)+"x)")
			else: 
				print("\t"+string)
	def figureOutMessage(self,observations):	
		message = readMessage(observations)	
		
		if message.find("This door is locked.") != -1:
			self.state.get("map").poke(observations, "locked")
		if self.phase != 0:
			return -1
		if message == "":
			# no message
			self.phase += 1
			return -1
		
		if message.find("You can't move diagonally into an intact doorway.") != -1:
			self.state.get("map").poke(observations, "baddoor")
		
		if message.find("You are carrying too much to get through.") != -1:
			self.state.get("map").poke(observations, "baddiag")
		
		if observations["misc"][2]:
			message += " --More--"
		else:
			self.phase += 1
		
		if len(self.log) > 0 and self.log[-1][0] == message:
			self.log[-1][1] += 1
		else:
			self.log.append([message,1])
		return -1
	
	def returnToTop(self):
		self.phase = 0

def read(state, observations):
	return state.get("reader").figureOutMessage(observations)