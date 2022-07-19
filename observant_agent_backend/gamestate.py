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
		from .reader import MessageSecretary
		from .doctor import StatusChecker
		self.modules = {
			"time" : Stopwatch(self),
			"queue" : ActionQueue(self),
			"reader" : MessageSecretary(self),
			"tracker" : MonsterTracker(self),
			"map" : Gazetteer(self),
			"doctor" : StatusChecker(self)
		}
	def reset(self):
		for key in self.modules:
			self.modules[key].reset()
		if not CONST_QUIET:
			print("\x1b[0;0;40m----------RIP----------\x1b[0;0;0m")
	def dumpCore(self,message,observations=None):
		if CONST_QUIET:
			return
		print("\x1b[0;31m",end="")
		print(message, end="\n\x1b[0;0m")
		for key in self.modules:
			self.modules[key].dumpCore()
	def get(self,name):
		# Returns a reference to a module
		return self.modules[name]