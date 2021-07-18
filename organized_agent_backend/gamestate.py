import numpy as np

from .utilities import *
from .annoyances import * # for the purpose of tracking troubles

CONST_QUIET = False # Enable to silence all prints about gamestate
CONST_DEAD_END_MULT = 3 # Multiply the number of times dead end squares get searched by this value
CONST_DESPERATION_RATE = 3 # Amount by which to increment desperation
CONST_STATUS_UPDATE_PERIOD = 500 # Print the map out every <#> steps

class Gamestate(object):

    def __init__(self):
        """ INITIALIZE MAP """
        self.dmap = makeEmptyMap(30, "?")
        self.searchMap = makeEmptyMap(30, 0)
        
        """ INITIALIZE MISC VARIABLES """
        self.lastKnownLevel = 0
        self.lastKnownRow = 0 # of hero
        self.lastKnownCol = 0 # of hero
        self.lastDirection = " "
        self.queue = []
        self.desperation = 0 # controls behavior when there's no obvious path forward
        self.itemUnderfoot = ""
        self.stepsTaken = 0
        self.troubles = []
    
    def reset(self):
        """ INITIALIZE MAP """
        self.dmap = makeEmptyMap(30, "?")
        self.searchMap = makeEmptyMap(30, 0)
        
        """ INITIALIZE MISC VARIABLES """
        self.lastKnownLevel = 0
        self.lastKnownRow = 0 # of hero
        self.lastKnownCol = 0 # of hero
        self.lastDirection = " "
        self.queue = []
        self.itemUnderfoot = ""
        self.stepsTaken = 0
        self.troubles = []
    
    def popFromQueue(self):
        if len(self.queue) == 0:
            return -1
        action = self.queue[0]
        self.queue = self.queue[1:]
        return action
    
    def updateMap(self, observations, vision=-1):
        # Vision defines how far away we look when updating the map
        # By default, the whole map is updated
        # Lowering this may save runtime
        # TODO: Mark open doorways. I don't plan to try to close them, but we can't move diagonally through open doorways
        dlvl = readDungeonLevel(observations)
        self.stepsTaken += 1
        if self.stepsTaken % CONST_STATUS_UPDATE_PERIOD == 0:
            self.statusReport(observations)
        if dlvl != self.lastKnownLevel:
            # Don't update the map on the step level changes; NLE is wack on that step
            # I think that's actually fixed now? Eh, whatever
            self.resetDesperation()
            self.lastKnownLevel = dlvl
            self.itemUnderfoot = ""
            if not CONST_QUIET:
                print("Now entering floor ", end="")
                print(dlvl+1)
            return
        row = readHeroRow(observations)
        col = readHeroCol(observations)
        if row != self.lastKnownRow or col != self.lastKnownCol:
            self.itemUnderfoot = ""
        self.lastKnownRow = row
        self.lastKnownCol = col
        message = readMessage(observations)
        if vision == -1:
            for x in range(21):
                for y in range(79):
                    heroXDist = abs(row-x)
                    heroYDist = abs(col-y)
                    glyph, char = readSquare(observations, x, y)
                    self.dmap[dlvl][x][y] = updateMainMapSquare(self.dmap[dlvl][x][y], glyph, char, heroXDist, heroYDist, message)
        else:
            for x in range(vision*2+1):
                for y in range(vision*2+1):
                    heroXDist = abs(x - vision)
                    heroYDist = abs(y - vision)
                    currRow = row + x - vision # the row of the square we're about to update
                    currCol = col + y - vision # the col of the square we're about to update
                    glyph, char = readSquare(observations, x, y)
                    self.dmap[dlvl][currRow][currCol] = updateMainMapSquare(dmap[dlvl][x][y], glyph, char, heroXDist, heroYDist, message)
        #if message.find("You feel feverish") != -1:
        #    self.troubles.append(handleLycanthropy)
        #    print("\"" + message + "\"")
        if message.find("This door is locked.") != -1:
            # Figure out which door it was referring to
            # If the hero is stunned or confused, we might mark the wrong square, but it'll be corrected on the next update
            if self.lastDirection == "N" and row > 0: # north
                self.dmap[dlvl][row-1][col] = "+"
            if self.lastDirection == "E" and col < 78: # east
                self.dmap[dlvl][row][col+1] = "+"
            if self.lastDirection == "S" and row < 20: # south
                self.dmap[dlvl][row+1][col] = "+"
            if self.lastDirection == "W" and col > 0: # west
                self.dmap[dlvl][row][col-1] = "+"
        if message.find("You succeed in picking the lock.") != -1:
            # Figure out which door it was referring to
            # If the hero is stunned or confused, we might mark the wrong square, but it'll be corrected on the next update
            if self.lastDirection == "N" and row > 0: # north
                self.dmap[dlvl][row-1][col] = "."
            if self.lastDirection == "E" and col < 78: # east
                self.dmap[dlvl][row][col+1] = "."
            if self.lastDirection == "S" and row < 20: # south
                self.dmap[dlvl][row+1][col] = "."
            if self.lastDirection == "W" and col > 0: # west
                self.dmap[dlvl][row][col-1] = "."
    def readMap(self, row, col, dlvl=-1):
        if dlvl == -1:
            dlvl = self.lastKnownLevel
        return self.dmap[dlvl][row][col]
    def readSearchedMap(self, row, col, dlvl=-1):
        if dlvl == -1:
            dlvl = self.lastKnownLevel
        return self.searchMap[dlvl][row][col]
    def updateSearchedMap(self):
        row = self.lastKnownRow
        col = self.lastKnownCol
        dlvl = self.lastKnownLevel
        nearbyNonWalls = 0
        if row > 0 and self.dmap[dlvl][row-1][col] != "X":
            nearbyNonWalls += 1
        if row < 20 and self.dmap[dlvl][row+1][col] != "X":
            nearbyNonWalls += 1
        if col > 0 and self.dmap[dlvl][row][col-1] != "X":
            nearbyNonWalls += 1
        if col < 78 and self.dmap[dlvl][row][col+1] != "X":
            nearbyNonWalls += 1
            
        if nearbyNonWalls == 1:
            incrementBy = 1/CONST_DEAD_END_MULT
        else:
            incrementBy = 1
        self.updateSearchedMapSquare(dlvl, row, col)
        if row > 0:
            #self.updateSearchedMapSquare(dlvl, row-1, col)
            self.searchMap[dlvl][row-1][col] += incrementBy
        if row < 20:
            #self.updateSearchedMapSquare(dlvl, row+1, col)
            self.searchMap[dlvl][row+1][col] += incrementBy
        if col > 0:
            #self.updateSearchedMapSquare(dlvl, row, col-1)
            self.searchMap[dlvl][row][col-1] += incrementBy
        if col < 78:
            #self.updateSearchedMapSquare(dlvl, row, col+1)
            self.searchMap[dlvl][row][col+1] += incrementBy
        if row > 0 and col > 0:
            #self.updateSearchedMapSquare(dlvl, row-1, col-1)
            self.searchMap[dlvl][row-1][col-1] += incrementBy
        if row > 0 and col < 78:
            #self.updateSearchedMapSquare(dlvl, row-1, col+1)
            self.searchMap[dlvl][row-1][col+1] += incrementBy
        if row < 20 and col > 0:
            #self.updateSearchedMapSquare(dlvl, row+1, col-1)
            self.searchMap[dlvl][row+1][col-1] += incrementBy
        if row < 20 and col < 78:
            #self.updateSearchedMapSquare(dlvl, row+1, col+1)
            self.searchMap[dlvl][row+1][col+1] += incrementBy
        return
    def updateSearchedMapSquare(self, dlvl, row, col):
        # If this square is a dead end, defined as a square cardinally adjacent to exactly one non-wall square,
        # it's extremely likely there's a secret passage there.
        # That being the case, it merits checking extra times, so we only increment by a fraction.
        # FIXME: Check hero position, not square position.
        nearbyNonWalls = 0
        if row > 0 and self.dmap[dlvl][row-1][col] != "X":
            nearbyNonWalls += 1
        if row < 20 and self.dmap[dlvl][row+1][col] != "X":
            nearbyNonWalls += 1
        if col > 0 and self.dmap[dlvl][row][col-1] != "X":
            nearbyNonWalls += 1
        if col < 78 and self.dmap[dlvl][row][col+1] != "X":
            nearbyNonWalls += 1
        
        if nearbyNonWalls == 1:
            self.searchMap[dlvl][row][col] += 1/CONST_DEAD_END_MULT
        else:
            self.searchMap[dlvl][row][col] += 1
        return
    def statusReport(self, observations):
        self.printMap()
        print("\"" + readMessage(observations) + "\"\n")
        
    def coreDump(self, message, observations):
        # TODO
        # Something went wrong, and we need to figure out what
        # Vomit as much information as possible about the known gamestate
        if CONST_QUIET:
            return
        print(message)
        self.printMap()
        print("")
        for x in range(21):
            for y in range(79):
                print(self.readSearchedMap(x, y),end=" ")
            print("") # end line of printout
        print("")
    def incrementDesperation(self):
        self.desperation += CONST_DESPERATION_RATE
        return
    def resetDesperation(self):
        self.desperation = 0
        return
    def printMap(self):
        if CONST_QUIET:
            return
        print("Current map of floor ", end="")
        print(self.lastKnownLevel+1)
        for x in range(len(self.dmap[self.lastKnownLevel])):
            for y in range(len(self.dmap[self.lastKnownLevel][x])):
                print(self.dmap[self.lastKnownLevel][x][y],end="")
            print("") # end line of printout
        print("")
    
def makeEmptyMap(depth,default):
    # Returns a 3D array, dimensioned to correspond to the dungeon's squares
    # Depth is the number of floors you want this map to track
    dungeon = []
    for x in range(depth):
        level = []
        for y in range(21):
            row = []
            for z in range(79):
                row.append(default)
            level.append(row)
        dungeon.append(level)
    return dungeon

def updateMainMapSquare(previousMarking, observedGlyph, observedChar, heroXDist, heroYDist, message):
    isNearHero = (heroXDist <= 1 and heroYDist <= 1)
    isLockedOut = (message.find("This door is locked.") != -1)
    isUnlockedNow = (message.find("You succeed in picking the lock.") != -1)
    if previousMarking == ">":
        return previousMarking # Don't overwrite the stairs
    if previousMarking == "s":
        return previousMarking # If shopkeep didn't let you in before they won't let you in now
    if observedGlyph >= 2360 and observedGlyph <= 2370: # Explicit wall, such as the ones around rooms
        return "X"
    if observedGlyph == 2359:
        if isNearHero: # "Solid stone"; acts identically to walls
            return "X"
        else:
            return previousMarking # Unobserved; don't update map
    if observedChar == 62 or message.find("You see here stairs leading down.") != -1: # Stairs (or, maybe, a ladder) leading downward
        return ">"
    if (observedGlyph == 2374 or observedGlyph == 2375): # Door, either horizontal or vertical
        if previousMarking == "+":
            return "+" # We saw it was locked before. It's fair to assume it's still locked. 
        else:
            return "." # Each door deserves to have its doorknob rattled, at least.
    if observedChar == 96: # Boulder
        return "`"
    if observedGlyph == 2376: # Iron bars
       return "#"
    if observedGlyph >= 381 and observedGlyph <= 761: # Pet
        return "p"
    if observedGlyph == 28: # Floating eye
        return "e"
    if heroXDist == 0 and heroYDist == 0: # War, the outcast Rider (marked on map mostly for the sake of printing to screen)
        return "@"
    if observedChar == 94: # Trap
        return "^"
    if observedGlyph >= 1144 and observedGlyph <= 1524 and (previousMarking == "?" or previousMarking == "^"):
        return "^" # A corpse you just find laying around is very likely a trap
    if (observedGlyph >= 1907 and observedGlyph <= 2352) or (observedGlyph >= 1144 and observedGlyph <= 1524):
        if previousMarking != "@" and previousMarking != "-" and previousMarking != "~":
            # Ooh, loot! We should take a closer look...
            return "$"
        else:
            # We already took a closer look and decided not to bother. Move on.
            return "-"
    if observedGlyph == 267: # Shopkeeper
        if message.find("Will you please") != -1:
            return "s" # We have a pickaxe, so shopkeep won't let us in. Don't get your hopes up if shopkeep steps away for a moment
        else:
            return "~" # Do not try to fight the shopkeeper, he's too tough for a low-level hero like us
    if observedGlyph == 268 or observedGlyph == 270: # Vault guard or Oracle
        return "~" # Again, too tough to realistically fight
    if observedGlyph <= 380:
        return "&" # Monster whose type we don't have special procedures for. Roll for initiative or something
    return "." # Anything else we treat as open space