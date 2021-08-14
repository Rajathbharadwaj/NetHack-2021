#!/usr/bin/python

from .gamestate import StateModule
from .utilities import *
import time

# TODO TODO TODO TODO TODO

class Stopwatch(StateModule):
	agenda = []
	def __init__(self):
		self.startTime = time.clock_gettime(time.CLOCK_UPTIME_RAW)
		self.lastKnownTurn = 0
	def reset(self):
		currTime = time.clock_gettime(time.CLOCK_UPTIME_RAW)
		Hz = self.lastKnownTurn / (currTime - self.startTime)
		if not CONST_QUIET:
			print(self.lastKnownTurn,"turns taken at",Hz,"Hz.")
		self.startTime = currTime
		self.lastKnownTurn = 0
	def dumpCore(self):
		pass
	def updateTurns(self, turns):
		self.lastKnownTurn = turns