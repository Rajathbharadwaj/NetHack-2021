#!/usr/bin/python

from .utilities import *

def searchAndProceed(state, observations):
	return pathfind(state, observations)[0]

def pathfind(state, observations, target="$>?", permeability=isPassable):
	# Uses Dijkstra's algorithm to get to the nearest space that's marked as one of the items in target
	# TODO: Fix the fact that this function has the brain of a gridbug (doesn't move diagonally)
	row = readHeroRow(observations)
	col = readHeroCol(observations)
	if target.count(state.readMap(row,col)) > 0:
		# you idiot, you're standing on the thing you're looking for! aidsfdsjaflnjdsk
		return -1, state.readMap(row,col)
	
	investigated = []
	queue = []
	howToReach = []
	
	for j in range(21):
		rowArray = []
		reachedRowArray = []
		for k in range(79):
			rowArray.append(False) 
			reachedRowArray.append(None) # if somehow this gets returned we want to crash
		investigated.append(rowArray)
		howToReach.append(reachedRowArray) # what moves can take you to this space
		
	queue.append([row, col])
	
	while len(queue) > 0:
		currRow = queue[0][0]
		currCol = queue[0][1]
		queue = queue[1:] # pop the element at the front of the queue since we're looking at it now
		if investigated[currRow][currCol]: # don't investigate the same space twice, that's inefficient
			continue # if this path was faster we'd have investigated it before the other path
	
		investigated[currRow][currCol] = True
	
	
		# check south
		if currRow < 20 and target.count(state.readMap(currRow+1,currCol)) > 0:
			firstAction = howToReach[currRow][currCol]
			if firstAction == None:
				return 2, state.readMap(currRow+1,currCol)
			return firstAction, state.readMap(currRow+1,currCol)
		if currRow < 20 and permeability[state.readMap(currRow+1,currCol)]:
			if howToReach[currRow+1][currCol] == None and not investigated[currRow+1][currCol]:
				queue.append([currRow+1,currCol])
				if howToReach[currRow][currCol] == None:
					howToReach[currRow+1][currCol] = 2
				else:
					howToReach[currRow+1][currCol] = howToReach[currRow][currCol]
					
		# check east
		if currCol < 78 and target.count(state.readMap(currRow,currCol+1)) > 0:
			firstAction = howToReach[currRow][currCol]
			if firstAction == None:
				return 1, state.readMap(currRow,currCol+1)
			return firstAction, state.readMap(currRow,currCol+1)
		if currCol < 78 and permeability[state.readMap(currRow,currCol+1)]:
			if howToReach[currRow][currCol+1] == None and not investigated[currRow][currCol+1]:
				queue.append([currRow,currCol+1])
				if howToReach[currRow][currCol] == None:
					howToReach[currRow][currCol+1] = 1
				else:
					howToReach[currRow][currCol+1] = howToReach[currRow][currCol]
					
		# check north
		if currRow > 0 and target.count(state.readMap(currRow-1,currCol)) > 0:
			firstAction = howToReach[currRow][currCol]
			if firstAction == None:
				return 0, state.readMap(currRow-1,currCol)
			return firstAction, state.readMap(currRow-1,currCol)
		if currRow > 0 and permeability[state.readMap(currRow-1,currCol)]:
			if howToReach[currRow-1][currCol] == None and not investigated[currRow-1][currCol]:
				queue.append([currRow-1,currCol])
				if howToReach[currRow][currCol] == None:
					howToReach[currRow-1][currCol] = 0
				else:
					howToReach[currRow-1][currCol] = howToReach[currRow][currCol]
					
		# check west
		if currCol > 0 and target.count(state.readMap(currRow,currCol-1)) > 0:
			firstAction = howToReach[currRow][currCol]
			if firstAction == None:
				return 3, state.readMap(currRow,currCol-1)
			return firstAction, state.readMap(currRow,currCol-1)
		if currCol > 0 and permeability[state.readMap(currRow,currCol-1)]:
			if howToReach[currRow][currCol-1] == None and not investigated[currRow][currCol-1]:
				queue.append([currRow,currCol-1])
				if howToReach[currRow][currCol] == None:
					howToReach[currRow][currCol-1] = 3
				else:
					howToReach[currRow][currCol-1] = howToReach[currRow][currCol]
	# if we're here, there's no reachable target on this floor
	# what happens next is not this function's responsibility to decide
	return -1, ""