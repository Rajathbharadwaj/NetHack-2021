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
				firstMsg = self.log[0][0]
				identityPos = firstMsg.find("You are a ")
				if identityPos == -1:
					print("Too bad – agent's identity was obscured.")
				else:
					print("Agent was a",firstMsg[identityPos+len("You are a "):])
				print("Recent messages:")
				for string, streak in self.log[-3:]:
					alteredString = self.state.get("tracker").annotate(string)
					if streak > 1:
						print("\t"+alteredString+" \x1b[0;33m("+str(streak)+"x)\x1b[0;0m")
					else: 
						print("\t"+alteredString)
		self.log = []
		self.phase = 0
	def dumpCore(self):
		print("Recent messages:")
		for string, streak in self.log[-10:]:
			alteredString = self.state.get("tracker").annotate(string)
			if streak > 1:
				print("\t"+alteredString+" [0;33m("+str(streak)+"x)\x1b[0;0m")
			else: 
				print("\t"+alteredString)
	def figureOutMessage(self,observations):
		message = readMessage(observations)	
		
		if message == "":
			# no message
			return -1
		
		if message[0] == "#":
			# agent inputting extended command; not worth logging
			return -1
		
		if message[-29:] == "(For instructions type a '?')":
			# not worth logging
			return -1
		
		if message[:24] == "What do you want to call":
			# not worth logging
			return -1
		
		if message.find("This door is locked.") != -1:
			self.state.get("map").poke(observations, "locked")
		
		if message.find("You can't move diagonally into an intact doorway.") != -1:
			self.state.get("map").poke(observations, "baddoor")
		
		if message.find("You are carrying too much to get through.") != -1:
			self.state.get("map").poke(observations, "baddiag")
		
		if message.find("You try to move the boulder, but in vain.") != -1:
			self.state.get("map").poke(observations, "badboulder")
		
		if message.find("You hear a monster behind the boulder.") != -1:
			self.state.get("map").poke(observations, "blockedboulder")
		
		if observations["misc"][2]:
			message += " --More--"
		
		if len(self.log) > 0 and self.log[-1][0] == message:
			self.log[-1][1] += 1
		else:
			self.log.append([message,1])
		return -1
	
	def returnToTop(self):
		# Deprecated
		self.phase = 0

def read(state, observations):
	return state.get("reader").figureOutMessage(observations)