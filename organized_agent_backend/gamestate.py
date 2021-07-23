import numpy as np

from .utilities import *
from .annoyances import * # for the purpose of tracking troubles
from .narration import CONST_QUIET, CONST_STATUS_UPDATE_PERIOD, CONST_PRINT_MAP_DURING_FLOOR_TRANSITION

CONST_DEAD_END_MULT = 3 # Multiply the number of times dead end squares get searched by this value
CONST_DESPERATION_RATE = 3 # Amount by which to increment desperation

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
        self.narrationStatus = {
            "report_timer" : CONST_STATUS_UPDATE_PERIOD,
            "quit_game" : False,
            "hp_threshold" : 0, # 1 means agent reached half health, 2 means agent reached quarter health. Resets to 0 when healed to full health.
            "hunger_threshold" : 0, # Tracks hunger severity, we want to print exactly once when we reach Weak status
            "weight_threshold" : 0 # Tracks encumbrance severity, we want to print exactly once when we reach Burdened status
        }
        self.lastMessage = ""
        self.messageStreak = 0 # Used to track if we're stuck against a wall or something
    
    def reset(self):
        # Before we wipe the slate clean, we should dump core if we haven't already
        if not CONST_QUIET:
            if not self.narrationStatus["quit_game"]:
                self.coreDump("The agent dies...")
            print("---------RIP---------")
            print("")
            
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
        self.narrationStatus = {
            "report_timer" : CONST_STATUS_UPDATE_PERIOD,
            "quit_game" : False,
            "hp_threshold" : 0,
            "hunger_threshold" : 0,
            "weight_threshold" : 0
        }
        self.lastMessage = ""
        self.messageStreak = 0
    
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
        if dlvl != self.lastKnownLevel:
            # Don't update the map on the step level changes; NLE is wack on that step
            # I think that's actually fixed now? Eh, whatever
            self.resetDesperation()
            if not CONST_QUIET:
                if CONST_PRINT_MAP_DURING_FLOOR_TRANSITION:
                    self.printMap()
                print("Now entering floor ", end="")
                print(dlvl+1)
            self.lastKnownLevel = dlvl
            self.itemUnderfoot = ""
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
            # TODO "RODNEY": Enable diagonals
            # When you do, don't forget to modify lockpick behavior in annoyances.py, too!
            if self.lastDirection == "N" and row > 0: # north
                self.dmap[dlvl][row-1][col] = "+"
            if self.lastDirection == "E" and col < 78: # east
                self.dmap[dlvl][row][col+1] = "+"
            if self.lastDirection == "S" and row < 20: # south
                self.dmap[dlvl][row+1][col] = "+"
            if self.lastDirection == "W" and col > 0: # west
                self.dmap[dlvl][row][col-1] = "+"
        if message.find("You succeed in picking the lock.") != -1 or message.find("You succeed in unlocking the door.") != -1:
            # Figure out which door it was referring to
            # If the hero is stunned or confused, we might mark the wrong square, but it'll be corrected on the next update
            # TODO "RODNEY": Enable diagonals
            # When you do, don't forget to modify lockpick behavior in annoyances.py, too!
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
        dirs = iterableOverVicinity(returnDirections = True, x=row, y=col)
        for x in range(4): # Only iterate over the cardinal directions for this
            if dirs[x] == None:
                continue # out of bounds
            r, c, str = dirs[x]
            if self.readMap(r,c) == "X":
                nearbyNonWalls += 1
        
        if nearbyNonWalls == 1:
            incrementBy = 1/CONST_DEAD_END_MULT
        else:
            incrementBy = 1
        
        #self.updateSearchedMapSquare(dlvl, row, col)
        self.searchMap[dlvl][row][col] += incrementBy
        for x in range(8): # Now we iterate over all directions, including diagonal
            if dirs[x] == None:
                continue # out of bounds
            r, c, str = dirs[x]
            self.searchMap[dlvl][r][c] += incrementBy
        return
    def updateSearchedMapSquare(self, dlvl, row, col):
        # If this square is a dead end, defined as a square cardinally adjacent to exactly one non-wall square,
        # it's extremely likely there's a secret passage there.
        # That being the case, it merits checking extra times, so we only increment by a fraction.
        # This function is deprecated and will probably just be deleted soon, because it flat-out works wrong.
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
        self.narrationStatus["report_timer"] = CONST_STATUS_UPDATE_PERIOD
        
    def coreDump(self, message, observations=None):
        # TODO
        # Something went wrong, and we need to figure out what
        # Vomit as much information as possible about the known gamestate
        if CONST_QUIET:
            return
        print(message)
        self.printMap()
        # print("")
        if self.narrationStatus["quit_game"]:
            # We panicked, so let's show the "searched" table
            for x in range(21):
                for y in range(79):
                    #print(self.readSearchedMap(x, y),end=" ")
                    if self.readSearchedMap(x, y) == 0:
                        print(" ",end="")
                        continue
                    if self.readSearchedMap(x, y) <= 30:
                        print("s",end="")
                        continue
                    print("S",end="")
                print("") # end line of printout
            print("")
    def incrementDesperation(self):
        self.desperation += CONST_DESPERATION_RATE
        return
    def resetDesperation(self):
        self.desperation = 0
        return
    def printMap(self, dlvl=-1):
        if CONST_QUIET:
            return
        if dlvl == -1:
            dlvl = self.lastKnownLevel
        print("Current map of floor ", end="")
        print(dlvl+1)
        for x in range(len(self.dmap[dlvl])):
            for y in range(len(self.dmap[dlvl][x])):
                print(self.dmap[dlvl][x][y],end="")
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
    # TODO: If we're blind, we should handle this function quite differently.
        # We should keep previously marked monsters marked since they're probably still there
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
            # TODO: There is actually an odd interaction here that needs to be reviewed.
            # If we see a square that was labelled on our map as "&" (monster) reach here, that could mean one of two things.
                # Either we lost visual on the monster (in which case it's probably still there)
                # Or it's a monster that can walk through walls (in which case it's probably NOT still there)
            # Unfortunately I'm not sure how to tell these two cases apart
            # But fortunately we don't yet often encounter monsters that walk through walls
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