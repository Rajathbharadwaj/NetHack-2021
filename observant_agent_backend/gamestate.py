#!/usr/bin/python

# observant_agent

from abc import ABC, abstractmethod
from .agent_config import *

class StateModule(ABC):
	@abstractmethod
	def reset(self):
		pass
	@abstractmethod
	def dumpCore(self,observations):
		pass

class Gamestate(object):
	def __init__(self):
		from .behaviors import ActionQueue
		from .tracker import MonsterTracker
		from .map import Gazetteer
		from .time import Stopwatch
		self.modules = {
			"queue" : ActionQueue(),
			"tracker" : MonsterTracker(self),
			"map" : Gazetteer(self),
			"time" : Stopwatch()
		}
	def reset(self):
		for key in self.modules:
			self.modules[key].reset()
		if not CONST_QUIET:
			print("----------RIP----------")
	def dumpCore(self,message,observations=None):
		if CONST_QUIET:
			return
		print(message)
		for key in self.modules:
			self.modules[key].dumpCore()
	def get(self,name):
		# Returns a reference to a module
		return self.modules[name]