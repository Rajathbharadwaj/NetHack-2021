import numpy as np
from .gamestate import *
from .utilities import *

CONST_TREAT_UNKNOWN_AS_PASSABLE = True # I've never yet set this to false but I'm keeping the option right now – you never know

CONST_AGENDA = [] # Will be populated at the end of the file

def chooseAction(state, observations):
    # This is this file's equivalent of a main method.
    # For organization's sake, it really shouldn't be much more complicated than "call function, see if it returned an action, repeat"
    state.updateMap(observations)
    handleItemUnderfoot(state, observations)
    action = state.popFromQueue()
    if action != -1:
        return action
    for protocol in CONST_AGENDA:
        action = protocol(state,observations)
        if action >= 0 and action < 8:
            state.lastDirection = numericCompass[action]
        if action != -1:
            return action
    state.coreDump("Agent has panicked! (Its logic gives it no move to make.)",observations)
    state.queue = [7]
    return 65 # Quit, then next step, answer yes to "are you sure?"
    

def handleItemUnderfoot(state, observations):
    message = readMessage(observations)
    lootIndexInMessage = message.find("You see here ")
    if lootIndexInMessage != -1:
        parsedLoot = message[lootIndexInMessage+len("You see here "):]
        locatedPeriod = parsedLoot.find(".")
        parsedLoot = parsedLoot[:locatedPeriod]
        itemID, beatitude = identifyLoot(parsedLoot)
        if worthTaking(state, observations, itemID, beatitude):
            state.itemUnderfoot = parsedLoot
    return

def advancePrompts(state, observations):
    message = readMessage(observations)
    # If the game is waiting for the player to press enter, press enter
    if observations["misc"][2]:
        return 19
    # If the game is waiting for a y/n prompt, answer y.
    if observations["misc"][0]:
        return 7
    # If the game is waiting for a text prompt, just press enter and ask for the default for now.
    # At a later time we may try to come up with a coherent answer but we're a long way from being able to wish or genocide...
    # And rather than name items, we'd be better off just tracking ourselves what items were seen to have what effects.
    if observations["misc"][1]:
        return 19
    return -1

def considerDescendingStairs(state, observations):
    # If the hero is on the stairs, descend the stairs.
    # Right now, we always descend the stairs. But this line of code doesn't really fit anywhere else.
    if state.readMap(readHeroRow(observations),readHeroCol(observations)) == ">":
        return 17
    return -1

def checkForEmergencies(state, observations):
    # TODO
    return -1

def fightInMelee(state, observations):
    heroRow = readHeroRow(observations)
    heroCol = readHeroCol(observations)
    if heroRow > 0 and state.readMap(heroRow-1,heroCol) == "&":
        state.queue = [0] # north
        return 40
    if heroRow < 20 and state.readMap(heroRow+1,heroCol) == "&":
        state.queue = [2] # south
        return 40
    if heroCol > 0 and state.readMap(heroRow,heroCol-1) == "&":
        state.queue = [3] # west
        return 40
    if heroCol < 78 and state.readMap(heroRow,heroCol+1) == "&":
        state.queue = [1] # east
        return 40
    if heroRow > 0 and heroCol > 0 and state.readMap(heroRow-1,heroCol-1) == "&":
        state.queue = [7] # northwest
        return 40
    if heroRow < 20 and heroCol > 0 and state.readMap(heroRow+1,heroCol-1) == "&":
        state.queue = [6] # southwest
        return 40
    if heroRow > 0 and heroCol < 78 and state.readMap(heroRow-1,heroCol+1) == "&":
        state.queue = [4] # northeast
        return 40
    if heroRow < 20 and heroCol < 78 and state.readMap(heroRow+1,heroCol+1) == "&":
        state.queue = [5] # southeast
        return 40
    return -1

def routineCheckup(state, observations):
    # TODO: Evaluate your current condition – heal if appropriate, eat if you're hungry, etc.
    #if observations["blstats"][21] > 1:
        # Hero is hungry. Eat food!
        # TODO: Come back to this once we've reimplemented inventory management
        #comestibles, foodTypes, indices = self.searchInventory(observations, permafood)
        #for x in range(len(comestibles)):
        #    return 35, chr(comestibles[x]), state
        
    if state.itemUnderfoot != "":
        # There's something here worth picking up, so let's do that
        if not CONST_QUIET:
            print("Picked up:"+state.itemUnderfoot)
        state.itemUnderfoot = False
        return 61
    return -1

def resolveAnnoyances(state, observations):
    action = butcherFloatingEyes(state, observations)
    if action == -1:
        action = pickLocks(state, observations)
    return action

def butcherFloatingEyes(state, observations):
    # TODO: Come back to this once we've reimplemented inventory management
    return -1

def pickLocks(state, observations):
    # TODO: Come back to this once we've reimplemented inventory management
    return -1

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

def evaluateObstacles(state, observations):
    # TODO: Re-implement procedures to deal with locked doors
    if(state.desperation < CONST_DESPERATION_RATE):
        state.incrementDesperation()
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

def worthTaking(state, observations, itemID, beatitude):
    # TODO
    # Returns TRUE if we should take this item
    return False

CONST_AGENDA = [advancePrompts,
    considerDescendingStairs,
    checkForEmergencies,
    fightInMelee,
    routineCheckup,
    resolveAnnoyances,
    searchAndProceed,
    evaluateObstacles
]