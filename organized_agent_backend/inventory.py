#!/usr/bin/python

# To clarify: This file defines functions and behaviors related to collecting and using items.
# If you're looking for handy raw arrays organizing information related to items, items.py is the file you want.

from .items import *
from .gamestate import *
from .logicgrid import identifiables
from .utilities import *

# TODO: Add a function that tells you what weapon is wielded

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