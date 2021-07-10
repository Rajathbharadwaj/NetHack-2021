#!/usr/bin/python

# To clarify: This file defines functions and behaviors related to collecting and using items.
# If you're looking for handy raw arrays organizing information related to items, items.py is the file you want.

from .items import *
from .gamestate import *

def searchInventory(observations, desired):
	# Look in the inventory for an item whose glyph number is one of the ones in desired
	# If one or more is found, report their inventory slots and which glyph they are
	letters = []
	types = []
	indices = []
	for x in range(len(observations["inv_glyphs"])):
		for y in desired:
			if observations["inv_glyphs"][x] == y:
				letters.append(observations["inv_letters"][x])
				types.append(y)
				indices.append(x)
	return letters, types, indices

def readBUC(description):
	if description.find("unholy water") != -1:
		return "c"
	if description.find("cursed") != -1:
		return "c"
	if description.find("holy water") != -1:
		return "b"
	if description.find("blessed") != -1:
		return "b"
	if description.find("uncursed") != -1:
		return "u"
	return "?"

def identifyLoot(description):
	if description.find("for sale") != -1:
		return -1, "" # TODO: Interact with shops (for now we just make a point of not attempting to shoplift)
	if description.find("unholy water") != -1:
		return 2203, "c"
	if description.find("holy water") != -1:
		return 2203, "b"
	beatitude = readBUC(description)
	# TODO: Figure out how to tell if we're a priest
	# If we're a priest, we should always return "u" beatitude if we would otherwise return "?"
	# TODO: Figure out what to do with identified scrolls/potions/etc (they have a completely different name from any base name)
	for x in range(len(itemNames)):
		# We'll check the items in reverse order in the list
		# This is because generic versions of items (e.g. "arrow" vs "runed arrow") appear first but should be evaluated last
		# Otherwise all runed arrows will be treated as regular arrows!
		index = len(itemNames)-x-1
		if description.find(itemNames[index]) != -1:
			return itemLookup[index], beatitude
	return -1, ""

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