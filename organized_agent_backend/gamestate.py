import numpy as np

from .utilities import *
from .annoyances import * # for the purpose of tracking troubles
from .narration import CONST_QUIET, CONST_STATUS_UPDATE_PERIOD, CONST_PRINT_MAP_DURING_FLOOR_TRANSITION, CONST_REPORT_KILLS
from .logicgrid import *
from time import *
from random import * # spice up narration a bit

CONST_DEAD_END_MULT = 3 # Multiply the number of times dead end squares get searched by this value
CONST_DESPERATION_RATE = 3 # Amount by which to increment desperation

class Gamestate(object):

    def __init__(self):
        """ INITIALIZE MAP """
        self.dmap = makeEmptyMap(30, "?")
        self.searchMap = makeEmptyMap(30, 0)
        self.corpseMap = makeEmptyMap(30, [-1, -1])
        seed() # seed rng
        
        """ INITIALIZE MISC VARIABLES """
        self.lastKnownLevel = 0
        self.lastKnownRow = 0 # of hero
        self.lastKnownCol = 0 # of hero
        self.lastDirection = " "
        self.queue = []
        self.desperation = 0 # controls behavior when there's no obvious path forward
        self.itemUnderfoot = ""
        self.preyUnderfoot = ""
        self.stepsTaken = 0
        self.troubles = []
        self.narrationStatus = {
            "report_timer" : CONST_STATUS_UPDATE_PERIOD,
            "quit_game" : False,
            "hp_threshold" : 0, # 1 means agent reached half health, 2 means agent reached quarter health. Resets to 0 when healed to full health.
            "hunger_threshold" : 0, # Tracks hunger severity, we want to print exactly once when we reach Weak status
            "weight_threshold" : 0, # Tracks encumbrance severity, we want to print exactly once when we reach Burdened status
            "status" : [False] * 13 # Tracks each status ailment separately
        }
        self.lastMessage = ""
        self.messageStreak = 0 # Used to track if we're stuck against a wall or something
        self.identifications = {
            4 : LogicGrid(ringAppearances, ringActuals),
            5 : LogicGrid(amuletAppearances, amuletActuals),
            8 : LogicGrid(potionAppearances, potionActuals),
            9 : LogicGrid(scrollAppearances, scrollActuals),
            10 : LogicGrid(spellbookAppearances, spellbookActuals),
            11 : LogicGrid(wandAppearances, wandActuals)
        }
        self.episodeStartTime = clock_gettime(CLOCK_UPTIME_RAW)
    
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
        self.corpseMap = makeEmptyMap(30, [-1, -1])
        
        """ INITIALIZE MISC VARIABLES """
        self.lastKnownLevel = 0
        self.lastKnownRow = 0 # of hero
        self.lastKnownCol = 0 # of hero
        self.lastDirection = " "
        self.queue = []
        self.desperation = 0
        self.itemUnderfoot = ""
        self.preyUnderfoot = ""
        self.stepsTaken = 0
        self.troubles = []
        self.narrationStatus = {
            "report_timer" : CONST_STATUS_UPDATE_PERIOD,
            "quit_game" : False,
            "hp_threshold" : 0,
            "hunger_threshold" : 0,
            "weight_threshold" : 0,
            "status" : [False] * 13 # Tracks each status ailment separately
        }
        self.lastMessage = ""
        self.messageStreak = 0
        self.identifications = {
            4 : LogicGrid(ringAppearances, ringActuals),
            5 : LogicGrid(amuletAppearances, amuletActuals),
            8 : LogicGrid(potionAppearances, potionActuals),
            9 : LogicGrid(scrollAppearances, scrollActuals),
            10 : LogicGrid(spellbookAppearances, spellbookActuals),
            11 : LogicGrid(wandAppearances, wandActuals)
        }
        self.episodeStartTime = clock_gettime(CLOCK_UPTIME_RAW)
    
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
            # Floor changed
            self.resetDesperation()
            if not CONST_QUIET:
                if CONST_PRINT_MAP_DURING_FLOOR_TRANSITION:
                    self.printMap()
                print("Now entering floor ", end="")
                print(dlvl+1)
            self.lastKnownLevel = dlvl
            self.itemUnderfoot = ""
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
                    if currRow > 20 or currRow < 0 or currCol > 78 or currCol < 0:
                        continue
                    glyph, char = readSquare(observations, currRow, currCol)
                    self.dmap[dlvl][currRow][currCol] = updateMainMapSquare(self.dmap[dlvl][currRow][currCol], glyph, char, heroXDist, heroYDist, message)
        #if message.find("You feel feverish") != -1:
        #    self.troubles.append(handleLycanthropy)
        #    print("\"" + message + "\"")
        if message.find("This door is locked.") != -1:
            dirs = iterableOverVicinity(observations,True)
            for x in range(8):
                if dirs[x] == None:
                    continue # out of bounds
                row, col, str = dirs[x]
                if str == self.lastDirection:
                    self.dmap[dlvl][row][col] = "+"
                    break
        if message.find("You succeed in picking the lock.") != -1 or message.find("You succeed in unlocking the door.") != -1:
            dirs = iterableOverVicinity(observations,True)
            for x in range(8):
                if dirs[x] == None:
                    continue # out of bounds
                row, col, str = dirs[x]
                if str == self.lastDirection:
                    self.dmap[dlvl][row][col] = "."
                    break
        if message.find("It's a wall.") != -1 or message.find("It's solid stone.") != -1:
            dirs = iterableOverVicinity(observations,True)
            for x in range(8):
                if dirs[x] == None:
                    continue # out of bounds
                row, col, str = dirs[x]
                if str == self.lastDirection:
                    self.dmap[dlvl][row][col] = "*"
                    break
        corpseIndexInMessage = message.find("You kill the ")
        if corpseIndexInMessage != -1:
            # You may notice that we don't check for "you destroy the" messages.
            # AFAIK nothing that can possibly be created with that kind of message is safely edible,
            # and we're a long way from needing to sacrifice monsters at altars,
            # so such a corpse is useless to us.
            parsedCorpse = message[corpseIndexInMessage+len("You kill the "):]
            locatedMark = parsedCorpse.find("!")
            if locatedMark == -1:
                print("FATAL ERROR: \"you kill the\" message didn't end in a \"!\".")
                print("Culprit message: \"" + message + "\"")
                exit(1)
            
            parsedCorpse = (parsedCorpse[:locatedMark])
            if CONST_REPORT_KILLS and not CONST_QUIET:
                verb = "Killed"
                article = " a "
                firstLetter = parsedCorpse[0].lower()
                if firstLetter == "a" or firstLetter == "e" or firstLetter == "i" or firstLetter == "o" or firstLetter == "u":
                    article = " an "
                x = randint(1, 13)
                if x == 1:
                    verb = "Killed"
                if x == 2:
                    verb = "Pwned"
                if x == 3:
                    verb = "Slaughtered"
                if x == 4:
                    verb = "Terminated"
                if x == 5:
                    verb = "Smashed"
                if x == 6:
                    verb = "Deleted"
                if x == 7:
                    verb = "Executed"
                if x == 8:
                    verb = "Removed"
                if x == 9:
                    verb = "Took down"
                if x == 10:
                    verb = "Annihilated"
                if x == 11:
                    verb = "Purged"
                if x == 12:
                    verb = "Euthanized"
                if x == 13:
                    verb = "Ended"
                print(verb + article + parsedCorpse + ".")
            parsedCorpse += " corpse"
            corpseGlyph, trashcan = identifyLoot(parsedCorpse)
            dirs = iterableOverVicinity(observations,True)
            for x in range(8):
                if dirs[x] == None:
                    continue # out of bounds
                row, col, str = dirs[x]
                if str == self.lastDirection:
                    self.corpseMap[dlvl][row][col] = [corpseGlyph, readTurn(observations)+50]
                    break
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
        timeElapsed = clock_gettime(CLOCK_UPTIME_RAW) - self.episodeStartTime
        stepSpeed = self.stepsTaken / timeElapsed
        print(self.stepsTaken,end=" steps taken at an average of ")
        print(stepSpeed,end=" Hz.\n")
    def incrementDesperation(self):
        oldDesp = self.desperation
        self.desperation += CONST_DESPERATION_RATE
        if self.desperation >= 10 and oldDesp < 10 and not CONST_QUIET:
            print("Agent is a little desperate...")
        if self.desperation >= 20 and oldDesp < 20 and not CONST_QUIET:
            print("Agent is running out of ideas...")
        return
    def resetDesperation(self):
        if self.desperation >= 10 and not CONST_QUIET:
            print("Aha – somewhere new to explore!")
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
    def eliminate(self, appearance, actual, item_class):
        if item_class == 3:
            print("Fatal error: Attempted to identify armor. (Not yet supported)")
            print("Appearance: ",end="")
            print(appearance,end="; actual: ")
            print(actual,end="; function: eliminate (gamestate.py)\n")
            exit(1)
        self.identifications[item_class].eliminate(appearance, actual)
    def confirm(self, appearance, actual, item_class):
        if item_class == 3:
            print("Fatal error: Attempted to identify armor. (Not yet supported)")
            print("Appearance: ",end="")
            print(appearance,end="; actual: ")
            print(actual,end="; function: confirm (gamestate.py)\n")
            exit(1)
        self.identifications[item_class].confirm(appearance, actual)
    def markScrollExists(self, appearance):
        for x in range(20):
            # Rule out all the "dummy" possibilities for this scroll type
            self.identifications[9].eliminate(appearance, 20000+x)
    def checkIfIs(self, appearance, actual, item_class):
        if item_class == 3:
            print("Fatal error: Attempted to identify armor. (Not yet supported)")
            print("Appearance: ",end="")
            print(appearance,end="; actual: ")
            print(actual,end="; function: checkIfIs (gamestate.py)\n")
            exit(1)
        return self.identifications[item_class].isConfirmedAs(appearance, actual)
    def cacheInventory(self, observations):
        # When we're hallucinating, we need to use inv_strs to figure out what's what
        # But that's slow, so we only want to have to do this once per step,
        # rather than every time we want to search our inventory for something.
        # That's where this function comes in.
        self.cache = []
        for x in range(len(observations["inv_strs"])):
            if readInventoryItemDesc(observations, x) == "":
                self.cache.append(5976)
            self.cache.append(identifyLoot(readInventoryItemDesc(observations, x)))
    
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
    if observedGlyph == 2377: # Tree
        return "±"
    if observedGlyph == 2386: # Throne
        return "_"
    if observedGlyph == 2389: # Sink
        return "%"
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
        if previousMarking == "*":
            # Item is embedded in a wall. We generally can't move through walls.
            return "*"
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
    if observedGlyph == 268:
        print("Ooh, guard!")
    if observedGlyph == 268 or observedGlyph == 270: # Vault guard or Oracle
        return "~" # Again, too tough to realistically fight
    if observedGlyph <= 380:
        return "&" # Monster whose type we don't have special procedures for. Roll for initiative or something
    return "." # Anything else we treat as open space
    