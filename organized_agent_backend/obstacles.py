#!/usr/bin/python

from .utilities import *
from .gamestate import CONST_DESPERATION_RATE
from .proceed import pathfind
from .narration import CONST_QUIET
from .inventory import *

def evaluateObstacles(state, observations):
	if(state.desperation < CONST_DESPERATION_RATE):
		state.incrementDesperation()
	action = gropeForDoors(state, observations, state.desperation)
	while action == -1 and state.desperation < 10:
		state.incrementDesperation()
		action = gropeForDoors(state, observations, state.desperation)
	if action != -1:
		return action
	heroRow = readHeroRow(observations)
	heroCol = readHeroCol(observations)
	dirs = iterableOverVicinity(observations,True)
	for x in range(4): # When you take care of TODO "RODNEY" in gamestate.py, come back and change this to range(8)
		if dirs[x] == None:
			continue # out of bounds
		row, col, str = dirs[x]
		if state.readMap(row,col) == "+":
			if not CONST_QUIET:
				print("*KICKS DOWN DOOR*")
			state.queue = [x] # appropriate direction
			return 48 # kick
	
	# OK, at this point, we're desperate enough that we're willing to kick down doors and step on traps.
	
	willingToPass = isPassable.copy()
	willingToPass["+"] = True
	willingToPass["^"] = True
	action = pathfind(state, observations, target=">?", permeability=willingToPass)[0]
	if action != -1:
		return action
	
	action = gropeForDoors(state, observations, state.desperation)
	while action == -1 and state.desperation < 30:
		state.incrementDesperation()
		action = gropeForDoors(state, observations, state.desperation)
	if action != -1:
		return action
	# Alright, if we're here, then we're right on the verge of panicking.
	# Before we do that, though, one last thing we'll try –
	# Let's check our inventory for something we can use to teleport.
	# Maybe we can teleport our way out of where we're stuck.
	salvation, teleTypes, indices = searchInventoryArtificial(state, observations, teleports)
	for x in range(len(salvation)):
		if not CONST_QUIET:
			print("Last resort before panicking. Attempting teleport!")
		if teleTypes[x] == 10093: # scroll of teleport
			state.queue = [keyLookup[chr(salvation[x])]]
			return 67 # read
		if teleTypes[x] == 10165: # wand of teleport
			state.queue = [keyLookup[chr(salvation[x])], 18] # target yourself
			return 96 # zap
	return -1

def gropeForDoors(state, observations, desperation, permeability=isPassable):
	# Similar to "explore" – not entirely, though
	# We're looking for a nearby wall we can search for secret doors
	# As "desperation" increases, we consider farther-away walls, and search more times
	# Desperation being # means search each wall within # moves # times each
	row = readHeroRow(observations)
	col = readHeroCol(observations)
	dirs = iterableOverVicinity(observations)
	for x in range(8):
		if dirs[x] == None:
			continue # out of bounds
		r, c = dirs[x]
		if state.readMap(r,c) == "X" and state.readSearchedMap(r, c) < desperation:
			state.updateSearchedMap()
			return 75
	
	investigated = []
	queue = []
	howToReach = []
	distance = []
	
	for j in range(21):
		rowArray = []
		reachedRowArray = []
		distArray = []
		for k in range(79):
			rowArray.append(False) 
			reachedRowArray.append(None) # if somehow this gets returned we want to crash
			distArray.append(0)
		investigated.append(rowArray)
		howToReach.append(reachedRowArray) # what moves can take you to this space
		distance.append(distArray)
		
	queue.append([row, col])
	
	while len(queue) > 0:
		currRow = queue[0][0]
		currCol = queue[0][1]
		queue = queue[1:] # pop the element at the front of the queue since we're looking at it now
		if investigated[currRow][currCol]: # don't investigate the same space twice, that's inefficient
			continue # if this path was faster we'd have investigated it before the other path
		if distance[currRow][currCol] > desperation: # Nothing found within the number of steps allowed
			return -1

		investigated[currRow][currCol] = True
		
		dirs = iterableOverVicinity(x=currRow,y=currCol)
		for x in range(4): # Only iterate over the cardinal directions
			# So... why do we only iterate over the cardinal directions?
			# Mostly cuz I'm scared of the agent trying to squeeze diagonally through walls and getting stuck
			# It can be solved tho, I just haven't done it yet
			# so uh... TODO
			if dirs[x] == None:
				continue # out of bounds
			r, c = dirs[x]
			if state.readMap(r,c) == "X" and state.readSearchedMap(r,c) < desperation:
				firstAction = howToReach[currRow][currCol]
				if firstAction == None:
					return x
				return firstAction
			if permeability[state.readMap(r,c)]:
				if howToReach[r][c] == None and not investigated[r][c]:
					queue.append([r,c])
					distance[r][c] = distance[currRow][currCol] + 1
				if howToReach[currRow][currCol] == None:
					howToReach[r][c] = x
				else:
					howToReach[r][c] = howToReach[currRow][currCol]
	# if we're here, there's no reachable target on this floor
	# what happens next is not this function's responsibility to decide
	return -1