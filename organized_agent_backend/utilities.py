import numpy as np
from .items import *
from nle import nethack
# NOTE: Do NOT import gamestate.py or behaviors.py or anything else like that.
# This is supposed to be easily imported without any worries of circular dependencies.

CONST_TREAT_UNKNOWN_AS_PASSABLE = True

isPassable = {
    "." : True,
    "?" : CONST_TREAT_UNKNOWN_AS_PASSABLE,
    "X" : False,
    "`" : False,
    "#" : False,
    "e" : False,
    "&" : True,
    "@" : True,
    "~" : False,
    "^" : False,
    "$" : True,
    "-" : True,
    "s" : False,
    "+" : False,
    ">" : True,
    "p" : True,
    "±" : False,
    "%" : True, # This is a sink, so if you're levitating, avoid!
    "_" : True,
    "*" : False
}

numericCompass = [
    "N",
    "E",
    "S",
    "W",
    "NE",
    "SE",
    "SW",
    "NW"
]

keyLookup = {
    "a" : 24,
    "b" : 6,
    "c" : 30,
    "d" : 33,
    "e" : 35,
    "f" : 39,
    "g" : 72,
    "h" : 3,
    "i" : 44,
    "j" : 2,
    "k" : 0,
    "l" : 1,
    "m" : 54,
    "n" : 5,
    "o" : 57,
    "p" : 60,
    "q" : 64,
    "r" : 67,
    "s" : 75,
    "t" : 83,
    "u" : 4,
    "v" : 90,
    "w" : 94,
    "x" : 79,
    "y" : 7,
    "z" : 96,
    "A" : 81,
    "B" : 14,
    "C" : 27,
    "D" : 34,
    "E" : 37,
    "F" : 40,
    "G" : 73,
    "H" : 11,
    "I" : 45,
    "J" : 10,
    "K" : 8,
    "L" : 9,
    "M" : 55,
    "N" : 13,
    "O" : 58,
    "P" : 63,
    "Q" : 66,
    "R" : 69,
    "S" : 74,
    "T" : 80,
    "U" : 12,
    "V" : 43,
    "W" : 91,
    "X" : 87,
    "Y" : 15,
    "Z" : 28,
    "." : 18,
    "," : 61,
    "<" : 16,
    ">" : 17,
    ";" : 51,
    "0" : 102,
    "1" : 103,
    "2" : 104,
    "3" : 105,
    "4" : 106,
    "5" : 107,
    "6" : 108,
    "7" : 109,
    "8" : 110,
    "9" : 111,
    "+" : 97,
    "-" : 98,
    " " : 99,
    "*" : 76,
    #"}" : 19, # represents enter ("}" serves no inherent purpose in nethack)
    #"{" : -1, # special character; represents an open slot in the queue
    "$" : 112 # Added to NLE after the fact
}

def readMessage(observations):
    return bytes(observations["message"]).decode('ascii').replace('\0','')

def readHeroCol(observations):
    return observations["blstats"][0]

def readHeroRow(observations):
    return observations["blstats"][1]

def readDungeonLevel(observations):
    # Subtract one so it lines up with our zero-indexed arrays
    return observations["blstats"][12]-1

def readSquare(observations, row, col):
    glyph = observations["glyphs"][row][col]
    char = observations["chars"][row][col]
    return glyph, char

def readBUC(description):
    # Moved here from inventory.py because it's a dependency of readInventoryGlyph which belongs here
    if description.find("unholy water") != -1:
        return "c"
    if description.find("cursed") != -1:
        return "c"
    if description.find("holy water") != -1:
        return "b"
    if description.find("blessed") != -1:
        return "b"
    if description.find("uncursed") != -1:
        return "u"
    return "?"

def identifyLoot(description):
    # Moved here from inventory.py because it's a dependency of readInventoryGlyph which belongs here
    if description.find("for sale") != -1:
        return -1, "" # TODO: Interact with shops (for now we just make a point of not attempting to shoplift)
    if description.find("unholy water") != -1:
        return 2203, "c"
    if description.find("holy water") != -1:
        return 2203, "b"
    beatitude = readBUC(description)
    # TODO: Figure out how to tell if we're a priest
    # If we're a priest, we should always return "u" beatitude if we would otherwise return "?"
    # TODO: Figure out what to do with identified scrolls/potions/etc (they have a completely different name from any base name)
    for x in range(len(itemNames)):
        # We'll check the items in reverse order in the list
        # This is because generic versions of items (e.g. "arrow" vs "runed arrow") appear first but should be evaluated last
        # Otherwise all runed arrows will be treated as regular arrows!
        index = len(itemNames)-x-1
        if description.find(itemNames[index]) != -1:
            return itemLookup[index], beatitude
    return -1, ""

def readInventoryGlyph(state, observations, index):
    if readHeroStatus(observations, 9): # Hallucination
        # If we're hallucinating, we can't just look at the glyph IDs, because they're compromised.
        # So instead we gotta figure out what's what by the description.
        # WARNING: Under these conditions, we return an item's confirmed identity,
        # whereas normally we'd return its appearance.
        return state.cache[index]
    return observations["inv_glyphs"][index]

def readInventoryItemDesc(observations, index):
    return bytes(observations["inv_strs"][index]).decode('ascii').replace('\0','')

def readInventoryItemClass(observations, index):
    return observations["inv_oclasses"][index]

def readHeroStatus(observations, statusToCheck):
    # Checks if the hero is afflicted with a specific status condition, indicated by number
    # Options are:
        # (0) Petrification
        # (1) Degeneration into slime
        # (2) Strangulation
        # (3) Food poisoning
        # (4) Disease
        # (5) Blindness
        # (6) Deafness
        # (7) Stunning
        # (8) Confusion
        # (9) Hallucination
        # (10) Levitation
        # (11) Flight
        # (12) Riding
    status = [
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_STONE),
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_SLIME),
        
        #bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_STRNGL),
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & 0x00000004),
        
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_FOODPOIS),
        
        #bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_TERMILL),
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & 0x00000010),
        
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_BLIND),
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_DEAF),
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_STUN),
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_CONF),
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_HALLU),
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_LEV),
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_FLY),
        bool(observations["blstats"][nethack.NLE_BL_CONDITION] & nethack.BL_MASK_RIDE)
    ]
    return status[statusToCheck]

def iterableOverVicinity(observations = [], returnDirections = False, x = -1, y = -1):
    # There are several situations where we want to check the eight squares surrounding us for some purpose or other.
    # This is
    # Kind of a pain to do, and very susceptible to copy-paste errors.
    # So let's functionize it! :D
    
    # This returns an iterable over the directions, with the following characteristics:
        # Type: Array
        # Shape: 8x2, with a couple exceptions:
            # if returnDirections is true, it's 8x3
            # some directions may be invalid if we're at map edge; if so, those elements are None instead of an array
        # The first value in each pair is the row, and the second is the column
        # The third, if requested, is the string to feed to the last known direction variable
    # Sorted by action number – array[0] is interacted with using action 0, array[1] using action 1, etc
    
    from .narration import CONST_QUIET
    
    output = []
    if observations != []:
        heroRow = readHeroRow(observations)
        heroCol = readHeroCol(observations)
    if x != -1:
        heroRow = x
    if y != -1:
        heroCol = y
    
    if (x != -1) == (observations != []) and not CONST_QUIET:
        print("Error code 666A – something that called function \"iterableOverVicinity\" gave it inconsistent arguments!")
    if (x != -1) != (y != -1) and not CONST_QUIET:
        print("Error code 666B – something that called function \"iterableOverVicinity\" gave it inconsistent arguments!")
    
    if heroRow > 0:
        if returnDirections:
            output.append([heroRow-1, heroCol, "N"])
        else:
            output.append([heroRow-1, heroCol])
    else:
        output.append(None)
    
    if heroCol < 78:
        if returnDirections:
            output.append([heroRow, heroCol+1, "E"])
        else:
            output.append([heroRow, heroCol+1])
    else:
        output.append(None)
    
    if heroRow < 20:
        if returnDirections:
            output.append([heroRow+1, heroCol, "S"])
        else:
            output.append([heroRow+1, heroCol])
    else:
        output.append(None)
    
    if heroCol > 0:
        if returnDirections:
            output.append([heroRow, heroCol-1, "W"])
        else:
            output.append([heroRow, heroCol-1])
    else:
        output.append(None)
    
    if heroRow > 0 and heroCol < 78:
        if returnDirections:
            output.append([heroRow-1, heroCol+1, "NE"])
        else:
            output.append([heroRow-1, heroCol+1])
    else:
        output.append(None)
    
    if heroRow < 20 and heroCol < 78:
        if returnDirections:
            output.append([heroRow+1, heroCol+1, "SE"])
        else:
            output.append([heroRow+1, heroCol+1])
    else:
        output.append(None)
    
    if heroRow < 20 and heroCol > 0:
        if returnDirections:
            output.append([heroRow+1, heroCol-1, "SW"])
        else:
            output.append([heroRow+1, heroCol-1])
    else:
        output.append(None)
    
    if heroRow > 0 and heroCol > 0:
        if returnDirections:
            output.append([heroRow-1, heroCol-1, "NW"])
        else:
            output.append([heroRow-1, heroCol-1])
    else:
        output.append(None)
        
    if len(output) != 8 and not CONST_QUIET:
        print("Error code 1337 – function \"iterableOverDirs\" (utilities.py) returned wrong-sized array!")
    return output