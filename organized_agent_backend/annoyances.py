#!/usr/bin/python

from .inventory import *
from .items import *
from .narration import CONST_QUIET

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
	dirs = iterableOverVicinity(observations,True)
	for x in range(4): # TODO: Go to gamestate.py and handle the TODO labelled "RODNEY"; then, come back and change this to range(8).
		if dirs[x] == None:
			continue # out of bounds
		row, col, str = dirs[x]
		if state.readMap(row,col) == "e":
			if not CONST_QUIET:
				print("Haha, agent has a blindfold! Perish, annoying floating eye!")
			state.lastDirection = str
			state.queue = [bestBlind, 40, x, 40, x, 69, bestBlind, 36] # "Put on what?": bestBlind, fight the eye twice, remove the blindfold
			return 63 # put on
	if direction == -1:
		return -1 # No floating eye in range.

def pickLocks(state, observations):
	handyLockpicks, types, indices = searchInventory(observations, lockpicks)
	if len(handyLockpicks) == 0:
		return -1 # No lockpick, move on with our lives
	# TODO: Pick the best lockpick available if we have more than one, right now we just pick whichever comes to hand first
	bestLockpick = keyLookup[chr(handyLockpicks[0])]
	# OK, if we're here we have a lockpick. But, do we have a door we can pick? (Chest lockpicking WILL happen someday. Not today tho.)
	heroRow = readHeroRow(observations)
	heroCol = readHeroCol(observations)
	dirs = iterableOverVicinity(observations,True)
	for x in range(4): # TODO: Go to gamestate.py and handle the TODO labelled "RODNEY"; then, come back and change this to range(8).
		if dirs[x] == None:
			continue # out of bounds
		row, col, str = dirs[x]
		if state.readMap(row,col) == "+":
			if not CONST_QUIET:
				print("Unlocking door with lock-pick in direction ",end="")
			state.lastDirection = str
			if not CONST_QUIET:
				print(str)
			state.queue = [bestLockpick, x] # "Apply what?": bestLockpick, "In what direction?": direction
			return 24 # apply
	return -1 # No locked door in range.


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