#!/usr/bin/python

# So, let me brainstorm some pathfinding routines I might want
# NOTE: All of the functions in this file operate under the assumption that #Terrain is active

from .utilities import *
from .agent_config import *

# Fix-up
# Repair an existing route, by aiming for any of the spaces left on the viable route,
# and then append the rest of the route we were following before to the "return to route" route

def pathfindFixUp(gazetteer, observations, prevActions, prevRoute):
	# GOAL: Get to any of the coordinate pairs en route
	# Returns a list of actions and a list of coordinates (in that order)
	heroRow, heroCol = readHeroPos(observations)
	try:
		index = prevRoute.index([heroRow,heroCol])
	except ValueError:
		pass
	else:
		# We're actually still on the path. We just skipped ahead.
		# So, we delete some of the front of the movement queue and call it a day.
		return prevActions[index:], prevRoute[index:]
	
	investigated = [([False] * 79)]
	route = [([None] * 79)]
	actions = [([None] * 79)]
	distance = [([0] * 79)]
	for x in range(20):
		# I'd love to multiply all these arrays by 20 but that gives us shallow copies of their rows
		# so we gotta do this the slightly clumsier way
		investigated.append(investigated[0].copy())
		route.append(route[0].copy())
		actions.append(actions[0].copy())
		distance.append(distance[0].copy())
	queue = [[heroRow,heroCol]]
	
	route[heroRow][heroCol] = []
	actions[heroRow][heroCol] = []
	
	while len(queue) > 0:
		row, col = queue[0]
		queue = queue[1:] # pop the element at the front of the queue since we're looking at it now
		if investigated[row][col]: # don't investigate the same space twice, that's inefficient
			continue # if this path was faster we'd have investigated it before the other path
		if distance[row][col] > CONST_MAX_ROUTE_REPAIR_DIST:
			# Repairing the route is taking too long. Let's just make a new one
			return None, None
		investigated[row][col] = True
		dirs = iterableOverVicinity(x=row,y=col)
		for x in range(8): 
			if dirs[x] == None:
				continue # out of bounds
			r, c = dirs[x]
			try:
				index = prevRoute.index([r,c])
			except ValueError:
				if gazetteer.isMovementPossible(observations,[row,col],[r,c]):
					if actions[r][c] == None:
						queue.append([r,c])
						distance[r][c] = distance[row][col] + 1
						actions[r][c] = actions[row][col] + [x]
						route[r][c] = route[row][col] + [[r,c]]
			else:
				# Aha, back on track.
				finalActions = actions[row][col] + [x] + prevActions[index:]
				finalRoute = route[row][col] + [[row,col]] + prevRoute[index:]
				return finalActions, finalRoute
	return None, None

# A*
# Efficiently draw up a route to a specific pair of coordinates using A*

def pathfindAStar(gazetteer, observations, target, start=[]):
	pass

# Djistrika's
# Examine the surrounding spaces until you see a square that looks like it's worth going for

def pathfindStandard(gazetteer, observations, goal):
	return forwardWeGo(gazetteer, observations)

def forwardWeGo(gazetteer, observations):
	# GOAL: Find the stairs or unexplored turf
	# Returns a list of actions and a list of coordinates (in that order)
	heroRow, heroCol = readHeroPos(observations)
	if gazetteer.readSquare(observations,heroRow,heroCol) == 2383:
		# we're... we're already there tho...
		return [], []
	
	investigated = [([False] * 79)]
	route = [([None] * 79)]
	actions = [([None] * 79)]
	distance = [([0] * 79)]
	for x in range(20):
		# I'd love to multiply all these arrays by 20 but that gives us shallow copies of their rows
		# so we gotta do this the slightly clumsier way
		investigated.append(investigated[0].copy())
		route.append(route[0].copy())
		actions.append(actions[0].copy())
		distance.append(distance[0].copy())
	queue = [[heroRow,heroCol]]
	
	route[heroRow][heroCol] = []
	actions[heroRow][heroCol] = []
	
	while len(queue) > 0:
		row, col = queue[0]
		queue = queue[1:] # pop the element at the front of the queue since we're looking at it now
		if investigated[row][col]: # don't investigate the same space twice, that's inefficient
			continue # if this path was faster we'd have investigated it before the other path
	
		investigated[row][col] = True
		dirs = iterableOverVicinity(x=row,y=col)
		for x in range(8): 
			if dirs[x] == None:
				continue # out of bounds
			r, c = dirs[x]
			if gazetteer.readSquare(observations,r,c) == 2359:
				# We don't want to route all the way to the unknown square, it could be hazardous
				# Going to the last known space before the unknown one will reveal it, then we can plan from there
				return actions[row][col], (route[row][col] + [[row,col]])
			if gazetteer.isMovementPossible(observations,[row,col],[r,c]):
				if actions[r][c] == None:
					queue.append([r,c])
					distance[r][c] = distance[row][col] + 1
					actions[r][c] = actions[row][col] + [x]
					route[r][c] = route[row][col] + [[row,col]]
				if gazetteer.readSquare(observations,r,c) == 2383:
					return actions[r][c], (route[r][c] + [[r,c]])
	return None, None
	
	
# TODO: More policies might be nice (don't forget to add them to pathfindStandard!)

# Desperation
# Move to the nearest square that we haven't yet searched to exhaustion,
# with the caveat that squares that aren't adjacent to walls don't qualify

def pathfindDesperate(gazetteer, observations, desperation):
	pass