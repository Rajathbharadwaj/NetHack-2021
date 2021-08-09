#!/usr/bin/python

from .utilities import *
from .inventory import *

def searchAndProceed(state, observations):
	willingToPass = isPassable.copy()
	# If we have a lockpick, we can get past locked doors
	if len(searchInventory(state, observations, lockpicks)[0]) > 0:
		willingToPass["+"] = True
	if len(searchInventory(state, observations, blinds)[0]) > 0:
		willingToPass["e"] = True
	if len(searchInventory(state, observations, pickaxes)[0]) > 0:
		willingToPass["`"] = True
	
	action, trashcan = pathfind(state, observations, target="$", permeability=willingToPass, searchRange=8)
	if action != -1:
		return action
	
	if state.desperation > 0 and state.stepsTaken % 10 != 0:
		# When we have any amount of desperation, that means there's no obvious way forward.
		# That's not entirely likely to change just on a whim. It can, but it probably won't.
		# So, it's wasteful to spend runtime looking for a directly available way forward every single step.
		# We'll check every ten steps instead, that should suffice.
		return -1
	
	action, target = pathfind(state, observations, permeability=willingToPass)
	if target == ">" or target == "?":
		state.resetDesperation()
	return action

def pathfind(state, observations, target="$>?", permeability=isPassable, searchRange=-1):
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
	
		investigated[currRow][currCol] = True
		
		if searchRange != -1 and searchRange < distance[currRow][currCol]:
			return -1, ""
		
		dirs = iterableOverVicinity(x=currRow,y=currCol)
		for x in range(4): # Only iterate over the cardinal directions
			# Why do we only iterate over the cardinal directions, you ask?
			# Mostly cuz I'm scared of the agent trying to squeeze diagonally through walls and getting stuck
			# It can be solved tho, I just haven't done it yet
			# so uh... TODO
			if dirs[x] == None:
				continue # out of bounds
			r, c = dirs[x]
			if target.count(state.readMap(r,c)) > 0:
				firstAction = howToReach[currRow][currCol]
				if firstAction == None:
					return x, state.readMap(r,c)
				return firstAction, state.readMap(r,c)
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
	return -1, ""