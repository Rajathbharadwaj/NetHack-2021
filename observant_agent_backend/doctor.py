#!/usr/bin/env python3

from .gamestate import StateModule
from .agent_config import *
from .utilities import *

class StatusChecker(StateModule):
	def __init__(self, state):
		self.currentAilments = []
		self.lastKnownStatus = 0
		self.lastKnownHunger = 0
	def reset(self): 
		if not CONST_QUIET:
			status = self.reportStatus()
			if not len(status) == 0:
				print("Status at death: ",self.reportStatus())
		self.currentAilments = []
		self.lastKnownStatus = 0
		self.lastKnownHunger = 0
	def dumpCore(self):
		status = self.reportStatus()
		if not len(status) == 0:
			print("Status at death: ",self.reportStatus())
	def recordStatus(self, observations):
		self.lastKnownStatus = observations["blstats"][nethack.NLE_BL_CONDITION]
		self.lastKnownHunger = observations["blstats"][nethack.NLE_BL_HUNGER]
		return -1
	def logAilment(self, ailment):
		if(not ailment in self.currentAilments):
			self.currentAilments.append(ailment)
	def checkAilment(self, ailment):
		return ailment in self.currentAilments
	def cureAilment(self, ailment):
		self.currentAilments.remove(ailment)
	def reportStatus(self):
		result = self.currentAilments.copy()
		if (self.lastKnownStatus & nethack.BL_MASK_STONE):
			result.append("Stoning")
		if (self.lastKnownStatus & nethack.BL_MASK_SLIME):
			result.append("Sliming")
		if (self.lastKnownStatus & nethack.BL_MASK_STRNGL):
			result.append("Strangled")
		if (self.lastKnownStatus & nethack.BL_MASK_FOODPOIS):
			result.append("Food Poisoning")
		if (self.lastKnownStatus & nethack.BL_MASK_TERMILL):
			result.append("Illness")
		if (self.lastKnownStatus & nethack.BL_MASK_BLIND):
			result.append("Blindness")
		if (self.lastKnownStatus & nethack.BL_MASK_DEAF):
			result.append("Deafness")
		if (self.lastKnownStatus & nethack.BL_MASK_STUN):
			result.append("Stunning")
		if (self.lastKnownStatus & nethack.BL_MASK_CONF):
			result.append("Confusion")
		if (self.lastKnownStatus & nethack.BL_MASK_HALLU):
			result.append("Hallucination")
		if (self.lastKnownStatus & nethack.BL_MASK_LEV):
			result.append("Levitation")
		if (self.lastKnownStatus & nethack.BL_MASK_FLY):
			result.append("Flight")
		if self.lastKnownHunger == 0:
			result.append("Satiation")
		if self.lastKnownHunger == 2:
			result.append("Hunger")
		if self.lastKnownHunger == 3:
			result.append("Severe Hunger")
		if self.lastKnownHunger >= 4:
			result.append("Starvation")
		return result

def checkup(state, observations):
	return state.get("doctor").recordStatus(observations)