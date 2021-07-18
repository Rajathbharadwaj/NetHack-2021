#!/usr/bin/python

from .inventory import *
from .items import *

def resolveAnnoyances(state, observations):
	# First, let's look at our troubles
	"""
	x = 0
	while x < len(state.troubles):
		action, isFixed = state.troubles[x](state, observations)
		if isFixed:
			# Remove the trouble
			# The next trouble after it moves back into the newly freed index x,
			# so we needn't increment x
			state.troubles = state.troubles[:x] + state.troubles[x+1:]
		else:
			x += 1
		if action != -1:
			return action
	"""
	# Now for a couple miscellaneous things worth checking
	action = butcherFloatingEyes(state, observations)
	if action == -1:
		action = pickLocks(state, observations)
	return action

def butcherFloatingEyes(state, observations):
	handyBlindfolds, types, indices = searchInventory(observations, blinds)
	if len(handyBlindfolds) == 0:
		return -1 # No blindfold, move on with our lives
	# TODO: Pick the best blindfold available if we have more than one, right now we just pick whichever comes to hand first
	# And also, probably, if we know the blindfold is cursed, don't put it on
	bestBlind = keyLookup[chr(handyBlindfolds[0])]
	# Blindfold: Check. But is there a floating eye?
	direction = -1
	heroRow = readHeroRow(observations)
	heroCol = readHeroCol(observations)
	if heroRow > 0 and state.readMap(heroRow-1,heroCol) == "e":
		state.lastDirection = "N"
		direction = 0 # north
	if heroRow < 20 and state.readMap(heroRow+1,heroCol) == "e":
		state.lastDirection = "S"
		direction = 2 # south
	if heroCol > 0 and state.readMap(heroRow,heroCol-1) == "e":
		state.lastDirection = "W"
		direction = 3 # west
	if heroCol < 78 and state.readMap(heroRow,heroCol+1) == "e":
		state.lastDirection = "E"
		direction = 1 # east
	if heroRow > 0 and heroCol > 0 and state.readMap(heroRow-1,heroCol-1) == "e":
		state.lastDirection = "NW"
		direction = 7 # northwest
	if heroRow < 20 and heroCol > 0 and state.readMap(heroRow+1,heroCol-1) == "e":
		state.lastDirection = "SW"
		direction = 6 # southwest
	if heroRow > 0 and heroCol < 78 and state.readMap(heroRow-1,heroCol+1) == "e":
		state.lastDirection = "NE"
		direction = 4 # northeast
	if heroRow < 20 and heroCol < 78 and state.readMap(heroRow+1,heroCol+1) == "e":
		state.lastDirection = "SE"
		direction = 5 # southeast
	if direction == -1:
		return -1 # No floating eye in range.
	
	# Floating eye target locked.
	state.queue = [bestBlind, 40, direction, 40, direction, 69, bestBlind, 36] # "Put on what?": bestBlind, fight the eye twice, remove the blindfold
	return 63 # put on

def pickLocks(state, observations):
	handyLockpicks, types, indices = searchInventory(observations, lockpicks)
	if len(handyLockpicks) == 0:
		return -1 # No lockpick, move on with our lives
	# TODO: Pick the best lockpick available if we have more than one, right now we just pick whichever comes to hand first
	bestLockpick = keyLookup[chr(handyLockpicks[0])]
	# OK, if we're here we have a lockpick. But, do we have a door we can pick? (Chest lockpicking WILL happen someday. Not today tho.)
	direction = -1
	heroRow = readHeroRow(observations)
	heroCol = readHeroCol(observations)
	if heroRow > 0 and state.readMap(heroRow-1,heroCol) == "+":
		state.lastDirection = "N"
		direction = 0 # north
	if heroRow < 20 and state.readMap(heroRow+1,heroCol) == "+":
		state.lastDirection = "S"
		direction = 2 # south
	if heroCol > 0 and state.readMap(heroRow,heroCol-1) == "+":
		state.lastDirection = "W"
		direction = 3 # west
	if heroCol < 78 and state.readMap(heroRow,heroCol+1) == "+":
		state.lastDirection = "E"
		direction = 1 # east
	"""
	if heroRow > 0 and heroCol > 0 and state.readMap(heroRow-1,heroCol-1) == "+":
		state.lastDirection = "NW"
		direction = 7 # northwest
	if heroRow < 20 and heroCol > 0 and state.readMap(heroRow+1,heroCol-1) == "+":
		state.lastDirection = "SW"
		direction = 6 # southwest
	if heroRow > 0 and heroCol < 78 and state.readMap(heroRow-1,heroCol+1) == "+":
		state.lastDirection = "NE"
		direction = 4 # northeast
	if heroRow < 20 and heroCol < 78 and state.readMap(heroRow+1,heroCol+1) == "+":
		state.lastDirection = "SE"
		direction = 5 # southeast
	"""
	if direction == -1:
		return -1 # No locked door in range.
	
	# Locked door detected. Let's bust it open, shall we?
	state.queue = [bestLockpick, direction] # "Apply what?": bestLockpick, "In what direction?": direction
	return 24 # apply


# Now we get into functions that I'll call "troubles".
# These represent problems that will persist until otherwise stated.
# Each one should take state and observations as input, in that order
# And each one should return two numbers – recommended action, and a bool saying whether or not the problem is solved
# We'll keep track of them by adding trouble functions to a special array in the gamestate

def handleLycanthropy(state, observations):
	# (Holy water is more versatile than wolfsbane,
	# so given the choice we'll use the wolfsbane and conserve the holy water)
	handyWolfsbane = searchInventory(observations, [2164])[0][0]
	if handyWolfsbane != -1:
		state.queue = [handyWolfsbane]
		return 35, True # Eat the wolfsbane – problem solved
	# No wolfsbane. Ok, maybe we have holy water?
	waterLetters, trashcan, waterIndices = searchInventory(observations, [2203])
	
	# These arrays represent all the water in our inventory,
	# regardless of beatitude. So, we'll need to check
	# for holy water specifically.
	
	for x in range(len(waterIndices)):
		if readBUC(observations["inv_strs"][x]) == "b":
			state.queue = waterLetters[x]
			return 64, True # Quaff the holy water – problem solved
	
	# No definitive cure found in our inventory.
	# At this time I have no interest in quaffing unidentified water hoping it's holy,
	# so I guess we just have to put up with lycanthropy for now.
	
	return -1, False # No recommendation – problem lingers