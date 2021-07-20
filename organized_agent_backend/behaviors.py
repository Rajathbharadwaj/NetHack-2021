import numpy as np
from .gamestate import *
from .utilities import *
from .inventory import *
from .annoyances import resolveAnnoyances
from .proceed import searchAndProceed, pathfind
from .obstacles import evaluateObstacles
from .ranged_combat import fightAtRange
from .narration import narrateGame, CONST_QUIET

CONST_TREAT_UNKNOWN_AS_PASSABLE = True # I've never yet set this to false but I'm keeping the option right now – you never know

CONST_AGENDA = [] # Array is populated at the end of this file

def chooseAction(state, observations):
    # This is this file's equivalent of a main method.
    # For organization's sake, it really shouldn't be much more complicated than "call function, see if it returned an action, repeat"
    state.updateMap(observations)
    handleItemUnderfoot(state, observations)
    narrateGame(state, observations)
    action = state.popFromQueue()
    if action != -1:
        return action
    #if(len(searchInventory(observations, blinds)[0]) == 0): # Uncomment this to startscum for a specific item
    #    state.queue = [7]
    #    return 65
    for protocol in CONST_AGENDA:
        action = protocol(state,observations)
        if action == None:
            print("Fatal error: Protocol didn't return anything.")
            print("Protocol at fault: ",end="")
            print(protocol)
            exit()
        if action >= 0 and action < 8 and protocol != advancePrompts:
            state.lastDirection = numericCompass[action]
        if action != -1:
            return action
    state.narrationStatus["quit_game"] = True
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
        if isWorthTaking(state, observations, itemID, beatitude):
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
    if observations["blstats"][21] > 1:
        # Hero is hungry. Eat food!
        comestibles, foodTypes, indices = searchInventory(observations, permafood)
        for x in range(len(comestibles)):
            state.queue = [keyLookup[chr(comestibles[x])]]
            return 35
        
    if state.itemUnderfoot != "":
        # There's something here worth picking up, so let's do that
        if not CONST_QUIET:
            print("Picked up: "+state.itemUnderfoot)
        state.itemUnderfoot = ""
        return 61
    return -1


CONST_AGENDA = [advancePrompts,
    considerDescendingStairs,
    checkForEmergencies,
    fightInMelee,
    fightAtRange,
    routineCheckup,
    resolveAnnoyances,
    searchAndProceed,
    evaluateObstacles
]