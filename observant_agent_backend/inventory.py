#!/usr/bin/env python3

from .gamestate import StateModule
from .agent_config import *
from .utilities import *

class ItemManager(StateModule):
	def __init__(self, state):
		self.state = state
	def reset(self): 
		if not CONST_QUIET:
			pass
		pass
	def dumpCore(self):
		pass
	def reachForItem(self, observations, desired):
		# Look in the inventory for an item whose glyph number is one of the ones in desired
		# If one or more is found, report their inventory slots and which glyph they are
		letters = []
		types = []
		indices = []
		for x in range(len(observations["inv_glyphs"])):
			for y in desired:
				if readInventoryGlyph(self.state, observations, x) == y:
					letters.append(observations["inv_letters"][x])
					types.append(y)
					indices.append(x)
		return letters, types, indices