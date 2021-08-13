#!/usr/bin/python

from .gamestate import StateModule
from .utilities import *
from .pathfind import *

class Gazetteer(StateModule):
	agenda = []
	def __init__(self, state):
		self.route = []
		self.movements = []
		self.state = state
		self.phase = 0
		self.lastKnownFloor = 0
		self.solidStone = chessboard4D()
		self.boulders = chessboard4D()
	def reset(self):
		self.route = []
		self.movements = []
		self.phase = 0
		self.lastKnownFloor = 0
		self.solidStone = chessboard4D()
		self.boulders = chessboard4D()
	def dumpCore(self):
		if self.route == None:
			print("Agent failed to find a path forward.")
			return
		if len(self.route) > 0:
			print("Agent was on a",len(self.route),"step path to ",end="")
			print(self.route[-1],end=".\n")
	def returnToTop(self):
		self.phase = 0
	def update(self, observations):
		return self.agenda[self.phase](self,observations)
	def watchVicinity(self, observations):
		row,col = readHeroPos(observations)
		dirs = iterableOverVicinity(observations=observations)
		for x in range(8): 
			if dirs[x] == None:
				continue # out of bounds
			r, c = dirs[x]
			if self.readSquare(observations, r, c) == 2353: # boulder
				dng = readDungeonNum(observations)
				dlvl = readDungeonLevel(observations)
				self.boulders[dng][dlvl][r][c] = True
		# TODO: Check underfoot
		self.phase += 1
		return self.agenda[self.phase](self,observations)
	def assess(self, observations):
		heroPos = readHeroPos(observations)
		if self.route == None:
			return -1 # We're screwed, panic
		if len(self.route) <= 1:
			# We've reached the end of the current path. Time to draw a new one.
			self.state.get("queue").append("te\nb") # command: Terrain (hide monsters and objects)
			self.phase += 2
			return 20 # extended command
		if [heroPos[0],heroPos[1]] != self.route[0]:
			# We're not where we thought we would be. Let's see how we can get back on track.
			self.state.get("queue").append("te\nb") # command: Terrain (hide monsters and objects)
			self.phase += 1
			return 20 # extended command
		# TODO: Consider looking farther ahead
		if not self.isMovementPossible(observations, self.route[0], self.route[1]):
			# Something impeded our progress along this route. Let's try something else
			
			self.route = self.route[1:] # Boot in the butt for the fixer-upper to get the memo that we want something ELSE
			self.movements = self.movements[1:]
			
			self.state.get("queue").append("te\nb") # command: Terrain (hide monsters and objects)
			self.phase += 1
			return 20 # extended command
		if readDungeonLevel(observations) != self.lastKnownFloor:
			# We found ourselves on a new floor unexpectedly. Time to draw a new route.
			self.state.get("queue").append("te\nb") # command: Terrain (hide monsters and objects)
			self.phase += 2
			self.lastKnownFloor = readDungeonLevel(observations)
			return 20 # extended command
		# We're good to go.
		return -1
	def repairRoute(self, observations):
		self.movements, self.route = pathfindFixUp(self, observations, self.movements, self.route)
		if self.movements == None:
			# Well, that didn't work. Time to construct a new route.
			self.phase += 1
			return self.agenda[self.phase](self,observations)
		self.returnToTop()
		self.phase += 1
		return 36 # escape (close out terrain view)
	def newRoute(self, observations):
		# TODO: Consider other policies
		self.movements, self.route = pathfindStandard(self, observations, None)
		if self.route == [] and self.movements == []:
			self.state.get("queue").append(17) # go down the stairs
			return 36
		self.returnToTop()
		self.phase += 1
		return 36 # escape (close out terrain view)
	agenda = [
		watchVicinity,
		assess,
		repairRoute,
		newRoute
	]
	def isMovementPossible(self, observations, start, end):
		# sort of assumes #TERRAIN is active
		# will usually work even when it's not, but don't count on it
		if(abs(end[0]-start[0]) > 1 or abs(end[0]-start[0]) < -1):
			# movement too far
			return False
		startGlyph = self.readSquare(observations, start[0], start[1])
		endGlyph = self.readSquare(observations, end[0], end[1])
		if (endGlyph >= 2360 and endGlyph <= 2370) or endGlyph == 2376 or endGlyph == 2377:
			# terrain is impassible
			return False
		isDiagonal = (end[0] != start[0] and end[1] != start[1])
		if (endGlyph >= 2372 and endGlyph <= 2375) or (startGlyph >= 2372 and startGlyph <= 2375) and isDiagonal:
			# can't move diagonally through doorways
			return False
		dng = readDungeonNum(observations)
		dlvl = readDungeonLevel(observations)
		if self.boulders[dng][dlvl][end[0]][end[1]]:
			return False
		return True
	def readSquare(self, observations, row, col):
		glyph = observations["glyphs"][row][col]
		heroRow, heroCol = readHeroPos(observations)
		dng = readDungeonNum(observations)
		dlvl = readDungeonLevel(observations)
		if glyph == 2359 and abs(row - heroRow) <= 1 and abs(col - heroCol) <= 1:
			self.solidStone[dng][dlvl][row][col] = True
		# TODO: If it's an important dungeon feature, record it
		if glyph == 2359 and self.solidStone[dng][dlvl][row][col]:
			return 2360 # It's solid stone, so report it as a wall
		return glyph
	def proceed(self):
		if self.movements == None or len(self.movements) == 0:
			return -1
		nextMovement = self.movements[0]
		self.route = self.route[1:]
		self.movements = self.movements[1:]
		return nextMovement
			

def checkPath(state, observations):
	return state.get("map").update(observations)

def proceed(state, observations):
	return state.get("map").proceed()


def chessboard4D(filler=False):
	output = [[filler] * 79]
	for x in range(20):
		output.append(output[0])
	output = [output]
	for x in range(53):
		output.append(output[0])
	output = [output]
	for x in range(8):
		output.append(output[0])
	return output