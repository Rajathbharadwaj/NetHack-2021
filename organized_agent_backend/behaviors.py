import numpy as np
from .gamestate import *
from .utilities import *
from .inventory import *
from .annoyances import resolveAnnoyances
from .proceed import searchAndProceed, pathfind
from .obstacles import evaluateObstacles
from .ranged_combat import fightAtRange
from .narration import narrateGame, CONST_QUIET
from .logicgrid import *

CONST_TREAT_UNKNOWN_AS_PASSABLE = True # I've never yet set this to false but I'm keeping the option right now – you never know
CONST_MESSAGE_STREAK_THRESHOLD = 200 # Panic if at least this many of the same message appear in a row
CONST_INVENTORY_REVIEW_FREQUENCY = 50 # Check inventory for formal identification every # steps

CONST_AGENDA = [] # Array is populated at the end of this file

def chooseAction(state, observations):
    # This is this file's equivalent of a main method.
    # For organization's sake, it really shouldn't be much more complicated than "call function, see if it returned an action, repeat"
    state.updateMap(observations)
    handleItemUnderfoot(state, observations)
    narrateGame(state, observations)
    passiveItemIdentification(state, observations)
    
    action = state.popFromQueue()
    if action != -1:
        return action
    #if(len(searchInventoryArtificial(state, observations, teleports)[0]) == 0): # Uncomment this to startscum for a specific item
    #    state.queue = [7]
    #    return 65
    for protocol in CONST_AGENDA:
        action = protocol(state,observations)
        if action == None:
            # This is a fatal error, so we print even if CONST_QUIET
            print("Fatal error: Protocol didn't return anything.")
            print("Protocol at fault: ",end="")
            print(protocol)
            exit(1)
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
    if observations["blstats"][10] * 4 < observations["blstats"][11]:
        # Hero is at critical HP! Do we have a healing potion?
        salvation, healTypes, indices = searchInventoryArtificial(state, observations, heals)
        for x in range(len(salvation)):
            if not CONST_QUIET:
                print("Drinking that wonderful liquid of salvation!")
            state.queue = [keyLookup[chr(salvation[x])]]
            return 64 # quaff
    return -1

def fightInMelee(state, observations):
    dirs = iterableOverVicinity(observations,True)
    for x in range(8):
        if dirs[x] == None:
            continue # out of bounds
        row, col, str = dirs[x]
        if state.readMap(row,col) == "&":
            state.queue = [x] # direction of monster
            return 40 # fight
    return -1

def routineCheckup(state, observations):
    # TODO: Evaluate your current condition – heal if appropriate, eat if you're hungry, etc.
    if observations["blstats"][21] > 1:
        # Hero is hungry. Eat food!
        comestibles, foodTypes, indices = searchInventory(observations, permafood)
        for x in range(len(comestibles)):
            state.queue = [keyLookup[chr(comestibles[x])]]
            return 35 # eat
        
    if state.itemUnderfoot != "":
        # There's something here worth picking up, so let's do that
        if not CONST_QUIET:
            print("Picked up: "+state.itemUnderfoot)
        state.itemUnderfoot = ""
        return 61 # pick up
    return -1

def evaluateMessageStreak(state, observations):
    if readMessage(observations) == "":
        state.lastMessage = ""
        state.messageStreak = 0
        return -1
    if readMessage(observations) == state.lastMessage:
        state.messageStreak += 1
    else:
        state.lastMessage = readMessage(observations)
        state.messageStreak = 0
    if state.messageStreak >= CONST_MESSAGE_STREAK_THRESHOLD:
        state.narrationStatus["quit_game"] = True
        state.coreDump("Agent has panicked! (Stuck in situation: \"" + readMessage(observations) + "\")",observations)
        state.queue = [7]
        return 65 # Quit, then next step, answer yes to "are you sure?"
    return -1

def passiveItemIdentification(state, observations):
    # Every 50 steps, check our inventory to see if anything got formally identified
    if state.stepsTaken % 50 != 1:
        return
    trashcan, types, indices = searchInventory(observations, identifiables)
    for x in range(len(indices)):
        desc = readInventoryItemDesc(observations, indices[x])
        oclass = readInventoryItemClass(observations, indices[x])
        descGlyph = identifyLoot(desc)[0]
        if descGlyph < 10000:
            continue
        state.identifications[oclass].confirm(types[x],descGlyph)


CONST_AGENDA = [advancePrompts,
    evaluateMessageStreak,
    considerDescendingStairs,
    checkForEmergencies,
    fightInMelee,
    fightAtRange,
    routineCheckup,
    resolveAnnoyances,
    searchAndProceed,
    evaluateObstacles
]