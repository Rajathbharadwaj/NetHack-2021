import numpy as np
from .items import *
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
    ">" : True
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

def searchInventory(self, observations, desired):
    # Look in the inventory for an item whose glyph number is one of the ones in desired
    # If one or more is found, report their inventory slots and which glyph they are
    letters = []
    types = []
    indices = []
    for x in range(len(observations["inv_glyphs"])):
        for y in desired:
            if observations["inv_glyphs"][x] == y:
                letters.append(observations["inv_letters"][x])
                types.append(y)
                indices.append(x)
    return letters, types, indices



def identifyLoot(description):
    if description.find("for sale") != -1:
        return -1, "" # TODO: Interact with shops (for now we just make a point of not attempting to shoplift)
    beatitude = "?" # b for blessed, u for uncursed, c for cursed, ? for unknown
    if description.find("cursed") != -1:
        beatitude = "c"
    if description.find("blessed") != -1:
        beatitude = "b"
    if description.find("uncursed") != -1:
        beatitude = "u"
    if description.find("unholy water") != -1:
        return 2203, "c"
    if description.find("holy water") != -1:
        return 2203, "b"
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