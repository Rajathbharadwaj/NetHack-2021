#!/usr/bin/python

# This is a work in progress – it's not yet seaworthy. I need to figure out how to fetch some of the values we need.
# TODO TODO TODO TODO TODO

from .spellcasting import *
import math

def canDoMagix(state,observations):
	# returns False if for any reason the hero is 100% barred from spellcasting anything at all
	
	# If we're stunned, we can't cast
	if readHeroStatus(observations, 7):
		return False
	# If we're getting strangled, we can't cast
	if readHeroStatus(observations, 2):
		return False
	# TODO: If we're polymorphed into a silent or headless form, we can't cast
	# TODO: If we're polymorphed into a form that can't speak clearly, we can't cast
	# TODO: If cursed items are welded to both our hands, we can't cast
	# If we're overtaxed, we can't cast
	if observations["blstats"][22] >= 4:
		return False
	# If we're confused, we can't cast, at least not to any actual effect
	if readHeroStatus(observations, 8):
		return False
	
	return True

def successfulSpellChance(state, observations, spellName):
	roleDetails = roleSpellcastingDatabase[state.role]
	spellDetails = spellDatabase[spellName]
	
	# TODO: If above function returns false, 0% chance to work
	# TODO: If hero is Weak or worse, and spellName is not detect food, 0% chance to work
	# TODO: If hero is strength 3, and spellName is not restore ability, 0% chance to work
	# TODO: If we don't know the spell or have forgotten it, 0% chance to work
	
	isWearingMetalBoots = False # TODO
	isWearingMetalHelm = False # TODO
	isWearingMetalGloves = False # TODO
	isWearingMetalSuit = False # TODO
	isWearingRobe = False # TODO
	isWearingShield = False # TODO
	isWearingLargeShield = False # TODO
	LOVE = state.lastKnownLOVE
	spellLevel = spellDetails["level"]
	skill = 0 # TODO
	
	penalty = roleDetails["base_penalty"]
	if spellDetails["is_emergency"]:
		penalty += roleDetails["emergency_modifier"]
	if isWearingShield:
		penalty += roleDetails["shield_penalty"]
	if isWearingMetalSuit and not isWearingRobe:
		penalty += roleDetails["mail_penalty"]
	if isWearingMetalSuit and isWearingRobe:
		penalty += math.floor(roleDetails["mail_penalty"] / 2)
	if isWearingRobe and not isWearingMetalSuit:
		penalty -= roleDetails["mail_penalty"]
	if isWearingMetalHelm:
		penalty += 4
	if isWearingMetalGloves:
		penalty += 6
	if isWearingMetalBoots:
		penalty += 2
	if roleDetails["specialty"] == spellName:
		penalty -= 4
	
	if penalty > 20:
		penalty = 20
	
	baseChance = floor(5.5 * observations[roleDetails["stat_used"]])
	
	difficulty = 4 * spellLevel - skill * 6 - floor(LOVE / 3) - 5
	
	chance = baseChance
	if difficulty > 0:
		chance -= floor(math.sqrt(900 * difficulty + 2000))
	if difficulty < 0:
		bonus = floor(difficulty * -15 / spellLevel)
		if bonus > 20:
			bonus = 20
		chance += bonus
	if chance < 0:
		chance = 0
	if chance > 120:
		chance = 120
	
	if isWearingLargeShield:
		if roleDetails["specialty"] == spellName:
			chance = floor(chance / 2)
		else:
			chance = floor(chance / 4)
	
	actualChance = floor(chance * (20 - penalty) / 15 - penalty)
	if actualChance > 100:
		actualChance = 100
	if actualChance < 0:
		actualChance = 0
	
	return actualChance / 100