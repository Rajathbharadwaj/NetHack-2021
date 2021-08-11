#!/usr/bin/python

# To clarify: This file defines functions and behaviors related to collecting and using items.
# If you're looking for handy raw arrays organizing information related to items, items.py is the file you want.

from .items import *
from .gamestate import *
from .logicgrid import identifiables
from .utilities import *
from .corpses import *

def searchInventory(state, observations, desired):
	# Look in the inventory for an item whose glyph number is one of the ones in desired
	# If one or more is found, report their inventory slots and which glyph they are
	letters = []
	types = []
	indices = []
	for x in range(len(observations["inv_glyphs"])):
		for y in desired:
			if readInventoryGlyph(state, observations, x) == y:
				letters.append(observations["inv_letters"][x])
				types.append(y)
				indices.append(x)
	return letters, types, indices

def searchInventoryArtificial(state, observations, desired):
	# Use this version to search for artificial glyph numbers
	letters = []
	types = []
	indices = []
	if readHeroStatus(observations, 9): # Hallucination
		# If we're hallucinating, we need to do things differently,
		# because the raw glyph IDs are not available.
		# Fortunately, when hallucinating,
		# searchInventory automatically goes by description,
		# which automatically yields items' identified states.
		# So a potion of healing would be marked as glyph 10063.
		
		# The downside is that while hallucinating,
		# we're dependent on the game to tell us what's what,
		# so if we're also afflicted with amnesia, we may miss
		# out on information that we recorded and could put to use.
		# But this isn't too big a concern...
		# amnesia + hallucination doesn't happen too often.

		return searchInventory(state, observations, desired)
	for x in range(len(observations["inv_glyphs"])):
		if not (observations["inv_glyphs"][x] in identifiables):
			continue
		oclass = readInventoryItemClass(observations, x)
		for y in desired:
			if state.checkIfIs(readInventoryGlyph(state, observations, x), y, oclass):
				letters.append(observations["inv_letters"][x])
				types.append(y)
				indices.append(x)
	return letters, types, indices

def isWorthTaking(state, observations, itemID, beatitude):
	# Returns TRUE if we should take this item
	for y in worthTaking:
		if itemID == y:
			return True
	if itemID >= 2056 and itemID <= 2094:
		return True # Rings and amulets are relatively lightweight, and once identified can be very useful
					# Rings especially – you can surrender a ring at a sink to precisely identify it, as long as you're not blind
	if itemID >= 2178 and itemID <= 2315:
		return True # Potions, scrolls, wands, and spellbooks are similarly useful
	return False

def isWorthMunching(state, observations, itemID, beatitude):
	# Returns TRUE if this corpse is worth eating from the floor
	# To be checked after isWorthTaking
	hunger = observations["blstats"][21]
	if itemID == 1299:
		# We like taking lichen corpses so this shouldn't come up much
		# But later on maybe the agent might have too much stuff to carry
		# in which case eating a lichen corpse rather than taking it makes sense
		return (hunger >= 1)
	
	# Now we think about corpses that are perishable.
	# Food poisoning is lethal, so we want to err on the side of caution.
	# We'll assume corpses are tainted unless we know for sure otherwise.
	
	row = readHeroRow(observations)
	col = readHeroCol(observations)
	dlvl = readDungeonLevel(observations)
	turn = readTurn(observations)
	approvedCorpse, expirationDate = state.corpseMap[dlvl][row][col]
	if beatitude == "b":
		expirationDate += 20
	if beatitude == "c":
		expirationDate -= 20
	# Corpses are uncursed by default, so it's safe to assume an unlabeled corpse is uncursed
	
	if turn > expirationDate:
		return False # missed our window of opportunity
	if approvedCorpse != itemID:
		return False # this isn't the corpse we saw die, so only gods know how old it actually is
	minPermissibleHunger = corpsePriority[itemID]
	if minPermissibleHunger <= hunger:
		return True
	else:
		return False

def whatIsWielded(state, observations):
	isHallu = readHeroStatus(observations, 9)
	letters = []
	types = []
	indices = []
	for x in range(len(observations["inv_glyphs"])):
		if readInventoryItemDesc(observations, x).find("(wielded)") != -1 or readInventoryItemDesc(observations, x).find("(weapon in hand") != -1:
			# By the way, the missing close paren in "(weapon in hand" is deliberate.
			# That way, we can hit "(weapon in hand)" and "(weapon in hands)" in one fell swoop
			letters.append(observations["inv_letters"][x])
			if isHallu:
				types.append(identifyLoot(readInventoryItemDesc(observations, x)))
			else:
				types.append(observations["inv_glyphs"][x])
			indices.append(x)
	return letters, types, indices

def whatIsWorn(state, observations):
	isHallu = readHeroStatus(observations, 9)
	letters = []
	types = []
	indices = []
	for x in range(len(observations["inv_glyphs"])):
		if readInventoryItemDesc(observations, x).find("(being worn)") != -1:
			letters.append(observations["inv_letters"][x])
			if isHallu:
				types.append(identifyLoot(readInventoryItemDesc(observations, x)))
			else:
				types.append(observations["inv_glyphs"][x])
			indices.append(x)
	return letters, types, indices