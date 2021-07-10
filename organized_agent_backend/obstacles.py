#!/usr/bin/python

from .utilities import *
from .gamestate import CONST_DESPERATION_RATE
from .proceed import pathfind

def evaluateObstacles(state, observations):
	# TODO: Re-implement procedures to deal with locked doors
	if(state.desperation < CONST_DESPERATION_RATE):
		state.incrementDesperation()
	action = gropeForDoors(state, observations, state.desperation)
	while action == -1 and state.desperation < 10:
		state.incrementDesperation()
		action = gropeForDoors(state, observations, state.desperation)
	heroRow = readHeroRow(observations)
	heroCol = readHeroCol(observations)
	if heroRow > 0 and state.readMap(heroRow-1,heroCol) == "+":
		state.queue = [0] # north
		return 48
	if heroRow < 20 and state.readMap(heroRow+1,heroCol) == "+":
		state.queue = [2] # south
		return 48
	if heroCol > 0 and state.readMap(heroRow,heroCol-1) == "+":
		state.queue = [3] # west
		return 48
	if heroCol < 78 and state.readMap(heroRow,heroCol+1) == "+":
		state.queue = [1] # east
		return 48
	if heroRow > 0 and heroCol > 0 and state.readMap(heroRow-1,heroCol-1) == "+":
		state.queue = [7] # northwest
		return 48
	if heroRow < 20 and heroCol > 0 and state.readMap(heroRow+1,heroCol-1) == "+":
		state.queue = [6] # southwest
		return 48
	if heroRow > 0 and heroCol < 78 and state.readMap(heroRow-1,heroCol+1) == "+":
		state.queue = [4] # northeast
		return 48
	if heroRow < 20 and heroCol < 78 and state.readMap(heroRow+1,heroCol+1) == "+":
		state.queue = [5] # southeast
		return 48
	
	action = pathfind(state, observations, target="+")
	
	action = gropeForDoors(state, observations, state.desperation)
	while action == -1 and state.desperation < 30:
		state.incrementDesperation()
		action = gropeForDoors(state, observations, state.desperation)
	return action

def gropeForDoors(state, observations, desperation, permeability=isPassable):
	# Similar to "explore" – not entirely, though
	# We're looking for a nearby wall we can search for secret doors
	# As "desperation" increases, we consider farther-away walls, and search more times
	# Desperation being # means search each wall within # moves # times each
	row = readHeroRow(observations)
	col = readHeroCol(observations)
	
	shouldJustSearch = False
	if row > 0 and state.readMap(row-1, col) == "X" and state.readSearchedMap(row-1, col) < desperation:
		shouldJustSearch = True
	if row < 20 and state.readMap(row+1, col) == "X" and state.readSearchedMap(row+1, col) < desperation:
		shouldJustSearch = True
	if col > 0 and state.readMap(row, col-1) == "X" and state.readSearchedMap(row, col-1) < desperation:
		shouldJustSearch = True
	if col < 78 and state.readMap(row, col+1) == "X" and state.readSearchedMap(row, col+1) < desperation:
		shouldJustSearch = True
	if row > 0 and col > 0 and state.readMap(row-1, col-1) == "X" and state.readSearchedMap(row-1, col-1) < desperation:
		shouldJustSearch = True
	if row > 0 and col < 78 and state.readMap(row-1, col+1) == "X" and state.readSearchedMap(row-1, col+1) < desperation:
		shouldJustSearch = True
	if row < 20 and col > 0 and state.readMap(row+1, col-1) == "X" and state.readSearchedMap(row+1, col-1) < desperation:
		shouldJustSearch = True
	if row < 20 and col < 78 and state.readMap(row+1, col+1) == "X" and state.readSearchedMap(row+1, col+1) < desperation:
		shouldJustSearch = True
		
	if shouldJustSearch:
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
		
	
		# check south
		if currRow < 20 and state.readMap(currRow+1,currCol) == "X" and state.readSearchedMap(currRow+1, currCol) < desperation:
			firstAction = howToReach[currRow][currCol]
			if firstAction == None:
				return 2
			return firstAction
		if currRow < 20 and permeability[state.readMap(currRow+1,currCol)]:
			if howToReach[currRow+1][currCol] == None and not investigated[currRow+1][currCol]:
				queue.append([currRow+1,currCol])
				distance[currRow+1][currCol] = distance[currRow][currCol]+1
				if howToReach[currRow][currCol] == None:
					howToReach[currRow+1][currCol] = 2
				else:
					howToReach[currRow+1][currCol] = howToReach[currRow][currCol]
					
		# check east
		if currCol < 78 and state.readMap(currRow,currCol+1) == "X" and state.readSearchedMap(currRow, currCol+1) < desperation:
			firstAction = howToReach[currRow][currCol]
			if firstAction == None:
				return 1
			return firstAction
		if currCol < 78 and permeability[state.readMap(currRow,currCol+1)]:
			if howToReach[currRow][currCol+1] == None and not investigated[currRow][currCol+1]:
				queue.append([currRow,currCol+1])
				distance[currRow][currCol+1] = distance[currRow][currCol]+1
				if howToReach[currRow][currCol] == None:
					howToReach[currRow][currCol+1] = 1
				else:
					howToReach[currRow][currCol+1] = howToReach[currRow][currCol]
					
		# check north
		if currRow > 0 and state.readMap(currRow-1,currCol) == "X" and state.readSearchedMap(currRow-1, currCol) < desperation:
			firstAction = howToReach[currRow][currCol]
			if firstAction == None:
				return 0
			return firstAction
		if currRow > 0 and permeability[state.readMap(currRow-1,currCol)]:
			if howToReach[currRow-1][currCol] == None and not investigated[currRow-1][currCol]:
				queue.append([currRow-1,currCol])
				distance[currRow-1][currCol] = distance[currRow][currCol]+1
				if howToReach[currRow][currCol] == None:
					howToReach[currRow-1][currCol] = 0
				else:
					howToReach[currRow-1][currCol] = howToReach[currRow][currCol]
					
		# check west
		if currCol > 0 and state.readMap(currRow,currCol-1) == "X" and state.readSearchedMap(currRow, currCol-1) < desperation:
			firstAction = howToReach[currRow][currCol]
			if firstAction == None:
				return 3
			return firstAction
		if currCol > 0 and permeability[state.readMap(currRow,currCol-1)]:
			if howToReach[currRow][currCol-1] == None and not investigated[currRow][currCol-1]:
				queue.append([currRow,currCol-1])
				distance[currRow][currCol-1] = distance[currRow][currCol]+1
				if howToReach[currRow][currCol] == None:
					howToReach[currRow][currCol-1] = 3
				else:
					howToReach[currRow][currCol-1] = howToReach[currRow][currCol]
					# if we're here, there's no reachable target on this floor
					# what happens next is not this function's responsibility to decide
	return -1