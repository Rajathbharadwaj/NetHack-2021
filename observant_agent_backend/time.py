#!/usr/bin/python

from .gamestate import StateModule
from .utilities import *
import time

class Stopwatch(StateModule):
	agenda = []
	def __init__(self, state):
		self.startTime = time.clock_gettime(time.CLOCK_UPTIME_RAW)
		self.lastKnownTurn = 1
		self.stepsThisTurn = 0
		self.state = state
		self.alreadyPanicked = False
	def reset(self):
		currTime = time.clock_gettime(time.CLOCK_UPTIME_RAW)
		Hz = self.lastKnownTurn / (currTime - self.startTime)
		if not CONST_QUIET:
			print(self.lastKnownTurn,"turns taken at",Hz,"Hz.")
		self.startTime = currTime
		self.lastKnownTurn = 1
		self.stepsThisTurn = 0
		self.alreadyPanicked = False
		if self.stepsThisTurn >= 1000:
			print(self.stepsThisTurn,"steps taken this turn.")
	def dumpCore(self):
		pass
	def updateTurns(self, turns):
		if self.lastKnownTurn != turns:
			self.stepsThisTurn = 0
		self.lastKnownTurn = turns
	def incrementTurns(self):
		self.lastKnownTurn += 1
		self.stepsThisTurn = 0
	def nextStep(self,observations):
		self.stepsThisTurn += 1
		if self.stepsThisTurn >= 900:
			x = 1
		if self.stepsThisTurn >= 1000 and not self.alreadyPanicked:
			# If *this* many steps happened without any time passing, it's a fair bet we're stuck.
			# So, rather than get wait to get slaughtered by the 10000 turn rule, let's dump core and quit.
			self.state.dumpCore("Agent has panicked! (1000 steps passed planning for one turn.)",observations)
			self.state.get("queue").cutInLine(7)
			self.state.get("queue").cutInLine(65)
			self.alreadyPanicked = True
			return 36 # Escape out of whatever we were doing, quit, and then next step, answer yes to "are you sure?"
		return -1

def countStep(state, observations):
	return state.get("time").nextStep(observations)