#!/usr/bin/python

# This is a work in progress – it's not yet seaworthy. I need to figure out how to fetch some of the values we need.
# TODO TODO TODO TODO TODO

from .spellcasting import *
from .items import *
from .inventory import *
from .utilities import *
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
	
	# TODO: If we don't know the spell or have forgotten it, 0% chance to work
	
	if not spellName in state.learnedSpells:
		# we haven't learned this spell
		return 0
	
	index = state.learnedSpells.index(spellName)
	if state.spellExpirations[index] < readTurn(observations):
		# we've forgotten this spell; trying to use it will just get us hit with stunning or confusion
		# TODO: If we get hit with amnesia, we'll need to figure out what spells we forgot
		# Trouble is, we'll need to read the 'cast spell' popup window for that, urghhh...
		return 0
	
	if not canDoMagix(state, observations):
		return 0
	
	if observations["blstats"][21] >= 3 and spellName != "detect food":
		# Hero is too hungry for magix, except detect food
		return 0
	
	if observations["blstats"][CONST_STRENGTH] <= 3 and spellName != "restore ability":
		# Hero is too weak for magix, except restore ability
		return 0
	
	if observations["blstats"][CONST_CURR_POWER] < 5 * spellDetails["level"]:
		# Can't pay the energy cost
		# Note to self: Come back here in a few years when we manage to get the amulet of yendor
		# cuz we'll need to take its energy drain into account on our way out of the dungeon
		return 0
	
	# And now, basically a line-by-line recreation of the formula used by the game to determine success chance...
	
	metalLoadout = checkWornMetal(state, observations)
	isWearingMetalBoots = metalLoadout[0]
	isWearingMetalHelm = metalLoadout[1]
	isWearingMetalGloves = metalLoadout[2]
	isWearingMetalSuit = metalLoadout[3]
	isWearingRobe = metalLoadout[4]
	isWearingSmallShield = metalLoadout[5]
	isWearingLargeShield = metalLoadout[6]
	LOVE = state.lastKnownLOVE
	spellLevel = spellDetails["level"]
	skill = state.skills.levelOfSkill(spellDetails["school"])
	
	penalty = roleDetails["base_penalty"]
	if spellDetails["is_emergency"]:
		penalty += roleDetails["emergency_modifier"]
	if isWearingSmallShield or isWearingLargeShield:
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
	
	baseChance = math.floor(5.5 * observations["blstats"][roleDetails["stat_used"]])
	
	difficulty = 4 * spellLevel - skill * 6 - math.floor(LOVE / 3) - 5
	
	chance = baseChance
	if difficulty > 0:
		chance -= math.floor(math.sqrt(900 * difficulty + 2000))
	if difficulty < 0:
		bonus = math.floor(difficulty * -15 / spellLevel)
		if bonus > 20:
			bonus = 20
		chance += bonus
	if chance < 0:
		chance = 0
	if chance > 120:
		chance = 120
	
	if isWearingLargeShield:
		if roleDetails["specialty"] == spellName:
			chance = math.floor(chance / 2)
		else:
			chance = math.floor(chance / 4)
	
	actualChance = math.floor(chance * (20 - penalty) / 15 - penalty)
	if actualChance > 100:
		actualChance = 100
	if actualChance < 0:
		actualChance = 0
	
	return actualChance / 100 # probability is expressed in decimal (so, 0 to 1, where 0 is 'impossible' and 1 is 'guaranteed')

def checkWornMetal(state, observations):
	
	# [0] isWearingMetalBoots
	# [1] isWearingMetalHelm
	# [2] isWearingMetalGloves
	# [3] isWearingMetalSuit
	# [4] isWearingRobe
	# [5] isWearingSmallShield
	# [6] isWearingLargeShield
	
	trashcan, types, indices = whatIsWorn(state, observations)
	metalLoadout = [False] * 7
	for x in range(len(types)):
		# Remember that we don't yet support armor identification
		# Revisit this function when we do, because:
			# Gauntlets of power and kicking boots are metal, even though their appearances aren't metal
			# Helms of brilliance are metal, but don't count as metal for spellcasting purposes
		if types[x] in metallicBoots: 
			# isWearingMetalBoots
			metalLoadout[0] = True
		if types[x] in metallicHelms:
			# isWearingMetalHelm
			metalLoadout[1] = True
		# Check for metallic gloves here at a later date
		# (the only metallic gloves are gauntlets of power)
		if types[x] in metallicMails:
			# isWearingMetalSuit
			metalLoadout[3] = True
		if types[x] in robes:
			# isWearingRobe
			metalLoadout[4] = True
		if types[x] in smallShields:
			# isWearingSmallShield
			metalLoadout[5] = True
		if types[x] in largeShields:
			# isWearingLargeShield
			metalLoadout[6] = True
	return metalLoadout

