#!/usr/bin/python

from .items import *
from .utilities import *
from .inventory import *

def fightAtRange(state, observations):
	action = throwProjectile(state, observations)[0]
	if action != -1:
		return action
	action = alignToThrow(state, observations)
	return action

def throwProjectile(state, observations, row=-1, col=-1, isHypothetical=False):
	# The first value returned is the suggested action
	# The second value returned is the distance to the target (we might want to maximize that, see alignToThrow)
	
	# isHypothetical, by the way, disables side effects (specificially, the side effect of queueing up the throw action)
	
	# First things first, do we have anything to shoot with?
	handyProjectiles, types, indices = searchInventory(observations, basicProjectiles)
	if len(handyProjectiles) == 0:
		return -1, -1 # No projectile, move on with our lives
	# TODO: Pick the best projectile available if we have more than one, right now we just pick whichever comes to hand first
	# FIXME: If we don't have a free hand, we get stuck, I think?
	bestProj = keyLookup[chr(handyProjectiles[0])]
	maxRange = miscObjectRange(state, observations)
	
	# Projectile armed. Do we have a suitable target?
	
	if row == -1:
		row = readHeroRow(observations)
	if col == -1:
		col = readHeroCol(observations)
	
	# Check north
	x = row - 1
	y = col
	farthestX = row - maxRange
	while x >= farthestX and x >= 0:
		icon = state.readMap(x,y)
		if icon == "&" or icon == "e":
			if not isHypothetical:
				state.queue = [bestProj, 0]
			return 83, row-x
		if icon == "X" or icon == "+" or icon == "~" or icon == "p":
			break
		x -= 1
		
	# Check northeast
	x = row - 1
	y = col + 1
	farthestX = row - maxRange
	while x >= farthestX and x >= 0 and y <= 78:
		icon = state.readMap(x,y)
		if icon == "&" or icon == "e":
			if not isHypothetical:
				state.queue = [bestProj, 4]
			return 83, row-x
		if icon == "X" or icon == "+" or icon == "~" or icon == "p":
			break
		x -= 1
		y += 1
	
	
	# Check east
	x = row 
	y = col + 1
	farthestY = col + maxRange
	while y <= farthestY and y <= 78:
		icon = state.readMap(x,y)
		if icon == "&" or icon == "e":
			if not isHypothetical:
				state.queue = [bestProj, 1]
			return 83, y-col
		if icon == "X" or icon == "+" or icon == "~" or icon == "p":
			break
		y += 1
	
	# Check southeast
	x = row + 1
	y = col + 1
	farthestX = row + maxRange
	while x <= farthestX and x <= 20 and y <= 78:
		icon = state.readMap(x,y)
		if icon == "&" or icon == "e":
			if not isHypothetical:
				state.queue = [bestProj, 5]
			return 83, x-row
		if icon == "X" or icon == "+" or icon == "~" or icon == "p":
			break
		x += 1
		y += 1
	
	# Check south
	x = row + 1
	y = col
	farthestX = row + maxRange
	while x <= farthestX and x <= 20:
		icon = state.readMap(x,y)
		if icon == "&" or icon == "e":
			if not isHypothetical:
				state.queue = [bestProj, 2]
			return 83, x-row
		if icon == "X" or icon == "+" or icon == "~" or icon == "p":
			break
		x += 1
	
	# Check southwest
	x = row + 1
	y = col - 1
	farthestX = row + maxRange
	while x <= farthestX and x <= 20 and y >= 0:
		icon = state.readMap(x,y)
		if icon == "&" or icon == "e":
			if not isHypothetical:
				state.queue = [bestProj, 6]
			return 83, x-row
		if icon == "X" or icon == "+" or icon == "~" or icon == "p":
			break
		x += 1
		y -= 1
	
	# Check west
	x = row
	y = col - 1
	farthestY = col - maxRange
	while y >= farthestY and y >= 0:
		icon = state.readMap(x,y)
		if icon == "&" or icon == "e":
			if not isHypothetical:
				state.queue = [bestProj, 3]
			return 83, col-y
		if icon == "X" or icon == "+" or icon == "~" or icon == "p":
			break
		y -= 1
	
	
	# Check northwest
	x = row - 1
	y = col - 1
	farthestX = row - maxRange
	while x >= farthestX and x >= 0 and y >= 0:
		icon = state.readMap(x,y)
		if icon == "&" or icon == "e":
			if not isHypothetical:
				state.queue = [bestProj, 7]
			return 83, row-x
		if icon == "X" or icon == "+" or icon == "~" or icon == "p":
			break
		x -= 1
		y -= 1
	
	# No target worth shooting
	return -1, -1
	

def alignToThrow(state, observations):
	# You can only throw in one of eight directions. So if the monster isn't in one of those directions, let's make it so!
	handyProjectiles, types, indices = searchInventory(observations, basicProjectiles)
	if len(handyProjectiles) == 0:
		return -1 # No projectile, move on with our lives
	
	# We want to maximize the distance between us and our target, so we can sneak in as many shots as possible before meleeing
	currAction = -1
	maxDist = 0
	# So let's consider our options

	row = readHeroRow(observations)
	col = readHeroCol(observations)
		
	# Check north
	x = row - 1
	y = col
	trashcan, dist = throwProjectile(state, observations, x, y, True)
	if isPassable[state.readMap(x,y)] and dist > maxDist:
		maxDist = dist
		currAction = 0 # move north
	
	# TODO: Check northeast
		# By the way, you may be wondering why I don't just... enable this code so we can move diagonally here.
		# It's not like it's bugged, per se...
		# But I'm worried enabling it will cause the agent to get stuck in a pattern like this:
		# @|
		# -.
		# You can only move to the "." if your encumbrance is low enough,
		# otherwise "you're carrying too much to get through".
		# That'd be an insta-stuck. That's bad.
	#x = row - 1
	#y = col + 1
	#trashcan, dist = throwProjectile(state, observations, x, y, True)
	#if isPassable[state.readMap(x,y)] and dist > maxDist:
	#	maxDist = dist
	#	currAction = 4 # move northeast
		
	# Check east
	x = row 
	y = col + 1
	trashcan, dist = throwProjectile(state, observations, x, y, True)
	if isPassable[state.readMap(x,y)] and dist > maxDist:
		maxDist = dist
		currAction = 1 # move east
		
	# TODO: Check southeast
	# x = row + 1
	# y = col + 1
	# trashcan, dist = throwProjectile(state, observations, x, y, True)
	# if isPassable[state.readMap(x,y)] and dist > maxDist:
	#	maxDist = dist
	#	currAction = 5 # move southeast
		
	# Check south
	x = row + 1
	y = col
	trashcan, dist = throwProjectile(state, observations, x, y, True)
	if isPassable[state.readMap(x,y)] and dist > maxDist:
		maxDist = dist
		currAction = 2 # move south
		
	# TODO: Check southwest
	# x = row + 1
	# y = col - 1
	# trashcan, dist = throwProjectile(state, observations, x, y, True)
	# if isPassable[state.readMap(x,y)] and dist > maxDist:
	#	maxDist = dist
	#	currAction = 6 # move southwest
		
	# Check west
	x = row
	y = col - 1
	trashcan, dist = throwProjectile(state, observations, x, y, True)
	if isPassable[state.readMap(x,y)] and dist > maxDist:
		maxDist = dist
		currAction = 3 # move west
		
		
	# TODO: Check northwest
	# x = row - 1
	# y = col - 1
	# trashcan, dist = throwProjectile(state, observations, x, y, True)
	# if isPassable[state.readMap(x,y)] and dist > maxDist:
	#	maxDist = dist
	#	currAction = 7 # move northwest
		
	return currAction

def crossbowRange(state, observations):
	return 8

def projectileRange(state, observations):
	# Use for launchers (bows, slings)
	strength = observations["blstats"][3]
	if strength <= 3:
		return 2
	if strength <= 5:
		return 3
	if strength <= 7: # TODO: If projectile is Aklys, return 4 (tether prevents it from going any farther)
		return 4
	if strength <= 9:
		return 5
	if strength <= 11:
		return 6
	if strength <= 13:
		return 7
	if strength <= 15:
		return 8
	if strength <= 17:
		return 9
	if strength <= 19:
		return 10
	if strength <= 21:
		return 11
	if strength <= 23:
		return 12
	return 13

def launcherlessProjectileRange(state, observations):
	# Use for arrows and bolts tossed by hand
	strength = observations["blstats"][3]
	if strength <= 3:
		return 0
	if strength <= 7:
		return 1
	if strength <= 11:
		return 2
	if strength <= 15:
		return 3
	if strength <= 19:
		return 4
	if strength <= 23:
		return 5
	return 6
	
def miscObjectRange(state, observations):
	# Use for anything not covered by the above two cases
	# The following objects need special cases (but in parentheses are the reasons I'm in no hurry to implement them):
		# Mjollnir (quest artifact; can only be thrown at all when strength is 25)
		# Boulder (only throwable when polymorphed into a giant)
		# Heavy Iron Ball (we don't currently get far enough to encounter punishment)
		# Loadstones (cursed loadstones can't be thrown, and loadstones have pitiful range and low damage anyway so why bother)
		# Objects that weigh 40 or more (Above cases aside, is there really anything this heavy that does anything useful when thrown?)
		# Underwater anything (We don't encounter deep water yet, and even if we did we'd need magical breathing for this to even apply)
	strength = observations["blstats"][3]
	if strength <= 3:
		return 1
	if strength <= 5:
		return 2
	if strength <= 7:
		return 3
	if strength <= 9:
		return 4
	if strength <= 11:
		return 5
	if strength <= 13:
		return 6
	if strength <= 15:
		return 7
	if strength <= 17:
		return 8
	if strength <= 19:
		return 9
	if strength <= 21:
		return 10
	if strength <= 23:
		return 11
	return 12