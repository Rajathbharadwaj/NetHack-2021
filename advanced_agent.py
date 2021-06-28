import numpy as np
from .keyLookup import *
from .items import *

from agents.base import BatchedAgent

CONST_TREAT_UNKNOWN_AS_PASSIBLE = True
CONST_MAP_STATUS_FREQUENCY = 1000
CONST_SHOW_MAP_ON_DEATH = False
CONST_SHOW_MAP_ON_PANIC = True
CONST_DESPERATION_THRESHOLD = 30 # Agent will panic if its desperation exceeds this value


# Here's a compass, just for reference...
# y k u
#  \|/
# h-.-l
#  /|\
# b j n

class AdvancedAgent(BatchedAgent):
    def __init__(self, num_envs, num_actions):
        """Set up and load you model here""" # joke's on you I'm not using ml here I'm too stupid for such smart person methods
        super().__init__(num_envs, num_actions)
        self.seeded_state = np.random.RandomState(42)
        
        # used to transition smoothly between floors
        self.lastFloor = []
        for x in range(num_envs):
            self.lastFloor.append(1)
        self.stepNum = []
        for x in range(num_envs):
            self.stepNum.append(0)
        self.state = []
        for x in range(num_envs):
            self.state.append([0,0,0,0,0,0,0,0,0,0])
        
        # useful for actions that take place over multiple turns
        # (message prompts, actions that need confirmation)
        self.queue = []
        for x in range(num_envs):
            self.queue.append("")
        
        # we map the dungeon ourselves to differentiate between walls and unexplored
        # and also so we can reference the map of one floor from another floor
            # (in case we want to backtrack to a sink, altar, etc.)
        
        self.map = []
        for i in range(num_envs):
            dungeon = []
            for j in range(30):
                floor = []
                for k in range(21):
                    row = []
                    for l in range(79):
                        row.append("?") # ? means "unexplored"
                    floor.append(row)
                dungeon.append(floor)
            self.map.append(dungeon)
        
        self.searched = []
        for i in range(num_envs):
            dungeon = []
            for j in range(30):
                floor = []
                for k in range(21):
                    row = []
                    for l in range(79):
                        row.append(0) # Any number means "searched # times"
                    floor.append(row)
                dungeon.append(floor)
            self.searched.append(dungeon)
        
    def batched_step(self, observations, rewards, dones, infos):
        """
        Perform a batched step on lists of environment outputs.

        Each argument is a list of the respective gym output.
        Returns an iterable of actions.
        """
        actions = self.handle_queue(dones)
        for x in range(self.num_envs):
            dlvl = observations[x]["blstats"][12]-1
            if self.state[x][1] == 1:
                self.map[x][dlvl], self.searched[x][dlvl] = self.update_map(self.lastFloor[x], observations[x], self.map[x][dlvl], self.searched[x][dlvl])
            else:
                self.map[x][dlvl], trashcan = self.update_map(self.lastFloor[x], observations[x], self.map[x][dlvl])
            self.lastFloor[x] = dlvl+1
            self.stepNum[x] += 1
            #if dones[x]:
                #print(bytes(observations[x]["message"]).decode('ascii').replace('\0',''))
            if self.stepNum[x] % CONST_MAP_STATUS_FREQUENCY == 0: # print the map every # steps
                print("CURRENT MAP OF FLOOR ", end="")
                print(dlvl+1)
                for y in range(21):
                    line = ""
                    for z in range(79):
                        line += self.map[x][dlvl][y][z]
                    print(line)
                print("\n\n")
            if actions[x] == -1:
                actions[x], self.queue[x], self.state[x] = self.choose_action(self.map[x], observations[x], rewards[x], dones[x], infos[x], self.state[x], self.searched[x])
            if self.state[x][1] == 1 or (len(self.queue[x]) > 0 and self.queue[x][0] == 's'):
                # update the searched map
                self.state[x][1] = 0
                y = observations[x]["blstats"][1]-1
                while y <= observations[x]["blstats"][1]+1:
                    z = observations[x]["blstats"][0]-1
                    while z <= observations[x]["blstats"][0]+1:
                        if(y >= 0 and y < 21 and z >= 0 and z < 79):
                            self.searched[x][dlvl][y][z] += 1
                        z += 1
                    y += 1
                            
        return actions
    
    def handle_queue(self, dones):
        actions = []
        for x in range(self.num_envs):
            if dones[x]:
                # Run over, reset the notebook for the next run
                self.lastFloor[x] = 1
                self.stepNum[x] = 0
                self.state[x] = [0,0,0,0,0,0,0,0,0,0]
                self.queue[x] = ""
                if CONST_SHOW_MAP_ON_DEATH:
                    # print the recorded map for debug purposes
                    print("\n\n")
                    for y in range(21):
                        line = ""
                        for z in range(79):
                            line += self.map[x][0][y][z]
                        print(line)
                    print("\n\n")
                # wipe the map clean
                dungeon = []
                for i in range(30):
                    floor = []
                    for j in range(21):
                        row = []
                        for k in range(79):
                            row.append("?") # ? means "unexplored"
                        floor.append(row)
                    dungeon.append(floor)
                self.map[x] = dungeon                
                dungeon = []
                for i in range(30):
                    floor = []
                    for j in range(21):
                        row = []
                        for k in range(79):
                            row.append(0) # Any number means "searched # times"
                        floor.append(row)
                    dungeon.append(floor)
                self.searched[x] = dungeon
                actions.append(-1)
                continue
            if self.queue[x] == "":
                actions.append(-1)
            else:
                actions.append(keyLookup[self.queue[x][0]])
                self.queue[x] = self.queue[x][1:] # pop the character we just handled from the queue
        return actions
    
    def update_map(self, lastFloor, observations, map, searched=[]):
        # Runs once per step (per active environment)
        # Feed in your current map and the observation suite the environment gives you
        # This function will return an updated map
        # TODO: Consider not checking every tile on every frame (to save runtime)? Maybe just ones near the hero?
        # TODO: Mark traps (anything that uses the character "^") and consider them impassible.
            # If a square that was unmarked before turns out to have a corpse on it, it's a fair assumption that it's a trap.
            # Statues are also usually traps, but they should be handled seperately, since healers can stethoscope them
        
        message = observations["message"]
        parsedMessage = bytes(message).decode('ascii').replace('\0','')
        heroRow = observations["blstats"][1]
        heroCol = observations["blstats"][0]
        
        descendMessage = "You descend the stairs." # Length 23
        cannotMessage = "You cannot" # Length 10
        lockedMessage = "This door is locked." # Length 20
        boulderMessage = "You try to move the boulder, but in vain." # Length 28
        unlockedMessage = "You succeed in picking the lock." # Length 32
        shouldntMessage = "Really attack " # Length 14
        
        isLockedOut = (parsedMessage[:20] == lockedMessage)
        isUnlockedNow = (parsedMessage[:32] == unlockedMessage)
        cantPush = (parsedMessage[:28] == boulderMessage)
        hesitate = (parsedMessage[:14] == shouldntMessage and message[14] >= 65 and message[14] <= 90)
            # If the game asks us to confirm before we attack a character with a capitalized name, it's probably a Bad Idea to attack them.
        if observations["blstats"][12] != lastFloor:
            print("Now entering floor ", end="")
            print(observations["blstats"][12])
            return map, searched # don't update the map on the step you change floor, the NLE observation is wack on that step
        screen = observations["chars"]
        for x in range(21):
            for y in range(79):
                if (screen[x][y] == 124 or screen[x][y] == 45) and observations["colors"][x][y] == 7: # Walls around rooms
                    map[x][y] = "X"
                    continue
                if(screen[x][y] == 96 and map[x][y] != "X"): # Boulders
                    if cantPush and abs(observations["blstats"][1] - x) <= 1 and abs(observations["blstats"][0] - y) <= 1:
                        map[x][y] = "X"
                        continue
                    map[x][y] = "`"
                    continue
                if screen[x][y] == 32: # Blank spaces that could either be still-unknown or corridor walls
                    if abs(observations["blstats"][1] - x) <= 1 and abs(observations["blstats"][0] - y) <= 1:
                        map[x][y] = "X"
                    continue
                if screen[x][y] == 62: # Stairs leading deeper
                    map[x][y] = ">"
                    continue
                if screen[x][y] == 43 and isLockedOut: # Locked doors
                    if abs(observations["blstats"][1] - x) <= 1 and abs(observations["blstats"][0] - y) <= 1:
                        map[x][y] = "+"
                        continue
                if screen[x][y] == 43 and isUnlockedNow: # Replace newly-unlocked doors with open spaces
                    if abs(observations["blstats"][1] - x) <= 1 and abs(observations["blstats"][0] - y) <= 1:
                        map[x][y] = "."
                        continue
                if screen[x][y] == 35 and observations["colors"][x][y] == 6: # iron bars
                    map[x][y] = "#"
                    continue
                if map[x][y] == ">": # don't overwrite where the stairs are marked
                    continue
                if observations["glyphs"][x][y] == 28:
                    map[x][y] = "e"
                    continue
                if x == observations["blstats"][1] and y == observations["blstats"][0]:
                    map[x][y] = "@"
                    continue
                if observations["chars"][x][y] != 35 and observations["glyphs"][x][y] != 267:
                    if x < 20 and map[x+1][y] == "s":
                        map[x][y] = "s"
                        continue
                    if y < 78 and map[x][y+1] == "s":
                        map[x][y] = "s"
                        continue
                    if x > 0 and map[x-1][y] == "s":
                        map[x][y] = "s"
                        continue
                    if y > 0 and map[x][y-1] == "s":
                        map[x][y] = "s"
                        continue
                if observations["glyphs"][x][y] >= 1907 and observations["glyphs"][x][y] <= 2352:
                    # Potential loot!
                    # (We could treat corpse glyphs as part of this category...
                    # corpses aren't too often worth lugging around, but they sometimes have items,
                    # and can be tinned with a tinning kit)
                    if map[x][y] == "s":
                        continue
                    if map[x][y] == "@":
                        map[x][y] = "-"
                    else:
                        map[x][y] = "$"
                    continue
                if observations["chars"][x][y] == 94: # trap
                    map[x][y] = "^"
                    continue
                if observations["glyphs"][x][y] >= 1144 and observations["glyphs"][x][y] <= 1524 and (map[x][y] == "?" or map[x][y] == "^"):
                    # corpse that was already there
                    # very strong hint that there's some sort of trap
                    map[x][y]
                    continue
                if observations["glyphs"][x][y] <= 380:
                    if hesitate and abs(observations["blstats"][1] - x) <= 1 and abs(observations["blstats"][0] - y) <= 1:
                        map[x][y] = "~"
                        continue
                    if observations["glyphs"][x][y] == 267:
                        # this incorrectly marks tiles as shop if the shopkeeper was generated from stone-to-flesh on a wished-for shopkeeper statue
                        # so uhhh
                        # don't do that
                        map[x][y] = "~"
                        map = self.markShopOnMap(map, x, y)
                        continue
                    map[x][y] = "&"
                    # We could add a failsafe that marks *all* monsters that yield the "Really attack the X?" message as peacefuls
                    # That would however cause major issues with peacefuls that don't stay in one place
                    # Besides, peacefuls can be killed with only minor issues, but attacking a shopkeeper is basically always YASD
                    
                    # Come to think of it, is there an easy way to tell if a monster is peaceful?
                    continue
                if observations["chars"][x][y] == 35:
                    map[x][y] = ","
                    continue
                if map[x][y] != ">" and (observations["chars"][x][y] != 43 or map[x][y] != "+") and map[x][y] != "s":
                    # open space, possibly with something in it that isn't as stalwart as a wall
                    map[x][y] = "."

        if searched != []:
            # we're searching, so let's update our map accordingly
            searched[heroRow][heroCol] += 1
            if heroRow < 21:
                searched[heroRow+1][heroCol] += 1
            if heroCol < 79:
                searched[heroRow][heroCol+1] += 1
            if heroRow > 0:
                searched[heroRow-1][heroCol] += 1
            if heroCol > 0:
                searched[heroRow][heroCol-1] += 1
            if heroRow > 0 and heroCol > 0:
                searched[heroRow+1][heroCol+1] += 1
            if heroRow > 0 and heroCol < 79:
                searched[heroRow+1][heroCol-1] += 1
            if heroRow < 21 and heroCol > 0:
                searched[heroRow-1][heroCol+1] += 1
            if heroRow < 21 and heroCol > 79:
                searched[heroRow-1][heroCol-1] += 1
        return map, searched
    
    def choose_action(self, dmap, observations, rewards, dones, infos, state, searched):
        message = observations["message"]
        parsedMessage = bytes(message).decode('ascii').replace('\0','')
        screen = observations["tty_chars"]
        heroRow = observations["blstats"][1]
        heroCol = observations["blstats"][0]
        dlvl = observations["blstats"][12]-1
        handyLockpick = self.searchInventory(observations, lockpicks)[0]
        if handyLockpick != None:
            handyLockpick = chr(handyLockpick)
        lockedMessage = "This door is locked." # Length 20
        shouldntMessage = "Really attack " # Length 14
        lootMessage = "You see here" # Length 11
        moreLootMessage = "Things " # Length 7
        bumLeftLegMessage = "Your left leg is in no shape for kicking."
        bumRightLegMessage = "Your right leg is in no shape for kicking."
        #if parsedMessage[:11] == lootMessage:
        #    x = 1 # break here so we know how this message is formatted
        #if parsedMessage[:7] == moreLootMessage:
        #    x = 1 # break here so we know how this message is formatted
        
        # Agent Name: Savvy Dungeoneer – Has a list of priorities he checks in order
        
        # If the game is waiting for the player to press enter, press enter
        if observations["misc"][2]:
            return 19, "", state
        # If the game is waiting for a y/n prompt, answer y.
        if observations["misc"][0]:
            if parsedMessage[:14] == shouldntMessage and message[14] >= 65 and message[14] <= 90:
                return 5, "", state # ...Unless we're about to attack a character with a capitalized name.
                                    # Most likely it's a shopkeeper, but honestly...
                                    # ...anything capitalized you're asked to confirm is probably gonna murder you.
            return 7, "", state
        # If the game is waiting for a text prompt, just press enter and ask for the default for now.
        if observations["misc"][1]:
            return 19, "", state
        # If the hero is on the stairs, descend the stairs.
        if dmap[dlvl][heroRow][heroCol] == ">":
            return 17, "", state
        
        # TODO: Check for emergencies.
            # If you're critically low on HP, heal.
            # If you're turning to stone, use a curative item, or pray if you have none.
            # If you're fainting, eat something.
            # If you're sliming, use a curative item, or pray if you have none.
            # If your intelligence is 3 (putting you at risk of brainlessness), restore it.
            # etc, etc
        
        # If there's a monster immediately adjacent to you, fight it so it doesn't just nibble on you
            # (Floating eyes, among other things, are to be ignored at this step.)
        
        if heroRow > 0 and dmap[dlvl][heroRow-1][heroCol] == "&":
            return 40, "k", state # north
        if heroRow < 20 and dmap[dlvl][heroRow+1][heroCol] == "&":
            return 40, "j", state # south
        if heroCol > 0 and dmap[dlvl][heroRow][heroCol-1] == "&":
            return 40, "h", state # west
        if heroCol < 78 and dmap[dlvl][heroRow][heroCol+1] == "&":
            return 40, "l", state # east
        if heroRow > 0 and heroCol > 0 and dmap[dlvl][heroRow-1][heroCol-1] == "&":
            return 40, "y", state # northwest
        if heroRow < 20 and heroCol > 0 and dmap[dlvl][heroRow+1][heroCol-1] == "&":
            return 40, "b", state # southwest
        if heroRow > 0 and heroCol < 78 and dmap[dlvl][heroRow-1][heroCol+1] == "&":
            return 40, "u", state # northeast
        if heroRow < 20 and heroCol < 78 and dmap[dlvl][heroRow+1][heroCol+1] == "&":
            return 40, "n", state # southeast
        
        
        # TODO: Evaluate your current condition – heal if appropriate, eat if you're hungry, etc.
        if observations["blstats"][21] > 1:
            # Hero is hungry. Eat food!
            comestible, trashcan = self.searchInventory(observations, permafood)
            if comestible != None:
                return 35, chr(comestible), state
        
        # TODO: If there's a floating eye immediately adjacent to you, see if you have a blindfold or towel handy.
        
        # TODO: If there's something near you that looks like it could come in handy, take a closer look
        
        # TODO: Appraise any items you happen to be standing on; take what's good, mark the rest as bad
        
        # TODO: Out of food? See if there's an edible monster nearby.
        
        # See if we can make use of a lockpick or credit card
        if handyLockpick != None:
            # Oooooh, we do indeed have a door-opener to work with. Let's see if there's something to pick.
            if heroRow > 0 and dmap[dlvl][heroRow-1][heroCol] == "+":
                return 24, handyLockpick+"k", state # north
            if heroRow < 21 and dmap[dlvl][heroRow+1][heroCol] == "+":
                return 24, handyLockpick+"j", state # south
            if heroCol > 0 and dmap[dlvl][heroRow][heroCol-1] == "+":
                return 24, handyLockpick+"h", state # west
            if heroCol < 79 and dmap[dlvl][heroRow][heroCol+1] == "+":
                return 24, handyLockpick+"l", state # east
            if heroRow > 0 and heroCol > 0 and dmap[dlvl][heroRow-1][heroCol-1] == "+":
                return 24, handyLockpick+"y", state # northwest
            if heroRow < 21 and heroCol > 0 and dmap[dlvl][heroRow+1][heroCol-1] == "+":
                return 24, handyLockpick+"b", state # southwest
            if heroRow > 0 and heroCol < 79 and dmap[dlvl][heroRow-1][heroCol+1] == "+":
                return 24, handyLockpick+"u", state # northeast
            if heroRow < 21 and heroCol < 79 and dmap[dlvl][heroRow+1][heroCol+1] == "+":
                return 24, handyLockpick+"n", state # southeast
        
        # Look for somewhere on the map we haven't been close enough yet to label, aim there
        # Or, if the stairs are nearer than anywhere new, just go for the stairs
        action, queue, target = self.explore(dmap[dlvl], heroRow, heroCol, ["?",">"])
        if action != -1:
            state[0] = 0 # reset desperation level to zero
            return action, "", state
        
        # TODO: Kill monsters, because maybe one of them is sitting on the stairs
        
        # TODO: With the obvious paths checked, maybe we can push one of the boulders?
        
        # TODO: ...Okay, see if there's a locked door on our map we can open. We'll kick it if need be.
        
        # TODO: Huh. Do we have Stone to Flesh? Maybe we can magic away a boulder to open up a new area.
            # Hm. We don't want to waste our energy converting a boulder that isn't actually blocking anyting.
        
        # Let's look for secret doors. Sometimes that's the only way to reach the stairs.
            # Not only is it actually pretty common for hidden passages to be the only way forward,
            # but also, hidden passages can very often remove the need to interact with boulders or diagonal passageways.
        if action == -1 and state[0] < 3:
            state[0] = 3 # start out searching each wall within 3 moves 3 tiles each
        
        while action == -1 and state[0] <= 9:
            action, queue = self.gropeForDoors(dmap[dlvl], searched[dlvl], heroRow, heroCol, state[0])
            if action == -1:
                state[0] += 3
        
        # TODO: Let's take a break from looking for secret doors to see if there's a door we can kick down.
        # We don't want to do this willy-nilly (we could get hurt, or get fined by a shopkeeper) but sometimes it's necessary
        
        if parsedMessage == bumLeftLegMessage or parsedMessage == bumRightLegMessage:
            return 18, "", state # wait for your leg to heal
        
        if action == -1:
            if heroRow > 0 and dmap[dlvl][heroRow-1][heroCol] == "+":
                return 48, "k", state # north
            if heroRow < 21 and dmap[dlvl][heroRow+1][heroCol] == "+":
                return 48, "j", state # south
            if heroCol > 0 and dmap[dlvl][heroRow][heroCol-1] == "+":
                return 48, "h", state # west
            if heroCol < 79 and dmap[dlvl][heroRow][heroCol+1] == "+":
                return 48, "l", state # east
            #if heroRow > 0 and heroCol > 0 and dmap[dlvl][heroRow-1][heroCol-1] == "+":
                #return 48, "y", state # northwest
            #if heroRow < 21 and heroCol > 0 and dmap[dlvl][heroRow+1][heroCol-1] == "+":
                #return 48, "b", state # southwest
            #if heroRow > 0 and heroCol < 79 and dmap[dlvl][heroRow-1][heroCol+1] == "+":
                #return 48, "u", state # northeast
            #if heroRow < 21 and heroCol < 79 and dmap[dlvl][heroRow+1][heroCol+1] == "+":
                #return 48, "n", state # southeast
        
            
        if action == -1:
            action, queue, target = self.explore(dmap[dlvl], heroRow, heroCol, ["+"])
            if action != -1:
                return action, "", state
        
        # OK back to looking for secret doors.
        
        while action == -1 and state[0] <= CONST_DESPERATION_THRESHOLD:
            action, queue = self.gropeForDoors(dmap[dlvl], searched[dlvl], heroRow, heroCol, state[0])
            if action == -1:
                state[0] += 3
        
        if action == 75:
            # we're about to search, so let's make a note to update the searched array
            state[1] = 1
        
        # TODO: Did one of the boulders say we couldn't push it because there was a monster on the other side? Let's wait it out.
            # Alternatively, if Stone to Flesh would be useful if only we had the energy for it, we can wait for our energy to refill.
        
        # TODO: Do we have a pickaxe we can try to use?
        
        # TODO: Uhhhhhh... iron bars can be destroyed, right?
        
        # Failing everything else, give up and quit the game
        # Print out the current floor's map so we can look into what happened
        if action == -1:
            print("Agent has panicked! (Its logic gives it no move to make.)")
            print("Floor panicked on: ", end="")
            print(dlvl+1)
            if not CONST_SHOW_MAP_ON_PANIC:
                return 65, "y", queue # just skip straight to sending the order to quit the game
            for y in range(21):
                line = ""
                for z in range(79):
                    if y == heroRow and z == heroCol:
                        line += "@"
                        continue
                    line += dmap[dlvl][y][z]
                print(line)
            print("\n\n")
            
            #print("Most recent observation:")
            #for x in range(21):
                #for y in range(79):
                    #print(observations["chars"][x][y],end=" ")
                #print("\n")
            return 65, "y", state
        return action, queue, state
    
    def isMapIconPassable(self, char):
        # TODO: Turn this into a dictionary, so we can change what we treat as passable if need be
        # chars correspond to our rendered map, not the raw observation table
        if char == ".": # Empty space, which may contain something we don't yet have a response for
            return True
        if char == ",": # Empty space, which may contain something we don't yet have a response for
            return True # This corresponds to dungeon corridor, which we track seperately to use as boundaries for shop turf
        if char == "?": # We haven't gotten close enough to this to see what it is
            return CONST_TREAT_UNKNOWN_AS_PASSIBLE
        if char == "X": # Wall
            return False
        if char == ">": # Stairs leading down
            return True
        if char == "+": # door that we've confirmed is locked
            return False
        if char == "`": # boulder; too complicated to bother with for right now
            return False
        if char == "#": # bars
            return False
        if char == "e": # floating eye; avoid!
            return False
        if char == "&": # generic monster; attack
            return True
        if char == "@": # the fourth Rider, War, theoretically the most dangerous
            return True
        if char == "~": # A shopkeeper, or other peaceful that doesn't merit messing with
            return False
        if char == "^": # A trap of some sort, better off avoided
            return False
        if char == "$": # Doesn't have to be money; can be any potentially useful item
            return True
        if char == "-": # We've seen what this is and decided not to take it; don't bother checking again
            return True
        if char == "s": # shop turf
            return True
        # Update me as needed!
    
    def explore(self, map, row, col, target):
        # Uses Dijkstra's algorithm to get to the nearest space that's marked as one of the items in target
        # TODO: Fix the fact that this function has the brain of a gridbug (doesn't move diagonally)
        
        if target.count(map[row][col]) > 0:
            # you idiot, you're standing on the thing you're looking for! aidsfdsjaflnjdsk
            return -1, "", map[row][col]
        
        investigated = []
        queue = []
        howToReach = []
        
        for j in range(21):
            rowArray = []
            reachRowArray = []
            for k in range(79):
                rowArray.append(False) 
                reachRowArray.append("")
            investigated.append(rowArray)
            howToReach.append(reachRowArray) # what moves can take you to this space
        
        queue.append([row, col])
        
        while len(queue) > 0:
            currRow = queue[0][0]
            currCol = queue[0][1]
            queue = queue[1:] # pop the element at the front of the queue since we're looking at it now
            if not investigated[currRow][currCol]: # don't investigate the same space twice, that's inefficient
                                                   # if this path was faster we'd have investigated it before the other path
                currSymbol = map[currRow][currCol]
                investigated[currRow][currCol] = True
                
                
                # check south
                if currRow < 20 and target.count(map[currRow+1][currCol]) > 0:
                    pathFound = howToReach[currRow][currCol] + "j"
                    firstAction = keyLookup[pathFound[0]]
                    if(map[currRow+1][currCol] == "?"):
                        pathFound = pathFound[1:0]
                        # don't blindly move onto the unknown space, it could be dangerous! just move next to it, that's enough to mark it
                    else:
                        pathFound = pathFound[1:]
                        # and in either case definitely remove the first instruction; we'll do it seperately and queue the others
                    return firstAction, pathFound, map[currRow+1][currCol]
                if currRow < 20 and self.isMapIconPassable(map[currRow+1][currCol]):
                    if howToReach[currRow+1][currCol] == "" and not investigated[currRow+1][currCol]:
                        queue.append([currRow+1,currCol])
                        howToReach[currRow+1][currCol] = howToReach[currRow][currCol] + "j"
                        
                # check east
                if currCol < 79 and target.count(map[currRow][currCol+1]) > 0:
                    pathFound = howToReach[currRow][currCol] + "l"
                    firstAction = keyLookup[pathFound[0]]
                    if(map[currRow][currCol+1] == "?"):
                        pathFound = pathFound[1:0]
                        # don't blindly move onto the unknown space, it could be dangerous! just move next to it, that's enough to mark it
                    else:
                        pathFound = pathFound[1:]
                        # and in either case definitely remove the first instruction; we'll do it seperately and queue the others
                    return firstAction, pathFound, map[currRow][currCol+1]
                if currCol < 79 and self.isMapIconPassable(map[currRow][currCol+1]):
                    if howToReach[currRow][currCol+1] == "" and not investigated[currRow][currCol+1]:
                        queue.append([currRow,currCol+1])
                        howToReach[currRow][currCol+1] = howToReach[currRow][currCol] + "l"
                        
                # check north
                if currRow > 0 and target.count(map[currRow-1][currCol]) > 0:
                    pathFound = howToReach[currRow][currCol] + "k"
                    firstAction = keyLookup[pathFound[0]]
                    if(map[currRow-1][currCol] == "?"):
                        pathFound = pathFound[1:0]
                        # don't blindly move onto the unknown space, it could be dangerous! just move next to it, that's enough to mark it
                    else:
                        pathFound = pathFound[1:]
                        # and in either case definitely remove the first instruction; we'll do it seperately and queue the others
                    return firstAction, pathFound, map[currRow-1][currCol]
                if currRow > 0 and self.isMapIconPassable(map[currRow-1][currCol]):
                    if howToReach[currRow-1][currCol] == "" and not investigated[currRow-1][currCol]:
                        queue.append([currRow-1,currCol])
                        howToReach[currRow-1][currCol] = howToReach[currRow][currCol] + "k"

                # check west
                if currCol > 0 and target.count(map[currRow][currCol-1]) > 0:
                    pathFound = howToReach[currRow][currCol] + "h"
                    firstAction = keyLookup[pathFound[0]]
                    if(map[currRow][currCol-1] == "?"):
                        pathFound = pathFound[1:0]
                        # don't blindly move onto the unknown space, it could be dangerous! just move next to it, that's enough to mark it
                    else:
                        pathFound = pathFound[1:]
                        # and in either case definitely remove the first instruction; we'll do it seperately and queue the others
                    return firstAction, pathFound, map[currRow][currCol-1]
                if currCol > 0 and self.isMapIconPassable(map[currRow][currCol-1]):
                    if howToReach[currRow][currCol-1] == "" and not investigated[currRow][currCol-1]:
                        queue.append([currRow,currCol-1])
                        howToReach[currRow][currCol-1] = howToReach[currRow][currCol] + "h"
        # if we're here, there's no reachable target on this floor
        # what happens next is not this function's responsibility to decide
        return -1, "", None
    
    def searchInventory(self, observations, desired):
        # Look in the inventory for an item whose glyph number is one of the ones in desired
        # If one is found, report its inventory slot and which glyph it is
        for x in range(len(observations["inv_glyphs"])):
            for y in desired:
                if observations["inv_glyphs"][x] == y:
                    return observations["inv_letters"][x], y
        return None, None
    
    def gropeForDoors(self, map, searched, row, col, desperation):
        # Similar to "explore" – not entirely, though
        # We're looking for a nearby wall we can search for secret doors
        # As "desperation" increases, we consider farther-away walls, and search more times
        # Desperation being # means search each wall within # moves # times each
        investigated = []
        queue = []
        howToReach = []
        
        for j in range(21):
            rowArray = []
            reachRowArray = []
            for k in range(79):
                rowArray.append(False) 
                reachRowArray.append("")
            investigated.append(rowArray) # -1 means "uninvestigated", other # means "investigated"
            howToReach.append(reachRowArray) # what moves can take you to this space
            
        queue.append([row, col])
        
        while len(queue) > 0:
            currRow = queue[0][0]
            currCol = queue[0][1]
            queue = queue[1:] # pop the element at the front of the queue since we're looking at it now
            if investigated[currRow][currCol] == False: # don't investigate the same space twice, that's inefficient
                                                      # if this path was faster we'd have investigated it before the other path
                if len(howToReach[currRow][currCol]) > desperation:
                    return -1, "" # We investigate paths in ascending order of length. This one's already too long, so we're done
                currSymbol = map[currRow][currCol]
                investigated[currRow][currCol] = True
            
                # check south
                if currRow < 20 and map[currRow+1][currCol] == "X" and searched[currRow+1][currCol] < desperation:
                    pathFound = howToReach[currRow][currCol] + "s"
                    firstAction = keyLookup[pathFound[0]]
                    pathFound = pathFound[1:] # Remove the first instruction; we'll do it seperately and queue the others
                    return firstAction, pathFound
                if currRow < 20 and self.isMapIconPassable(map[currRow+1][currCol]):
                    if howToReach[currRow+1][currCol] == "" and not investigated[currRow+1][currCol]:
                        queue.append([currRow+1,currCol])
                        howToReach[currRow+1][currCol] = howToReach[currRow][currCol] + "j"
                        
                # check east
                if currCol < 79 and map[currRow][currCol+1] == "X" and searched[currRow][currCol+1] < desperation:
                    pathFound = howToReach[currRow][currCol] + "s"
                    firstAction = keyLookup[pathFound[0]]
                    pathFound = pathFound[1:] # Remove the first instruction; we'll do it seperately and queue the others
                    return firstAction, pathFound
                if currCol < 79 and self.isMapIconPassable(map[currRow][currCol+1]):
                    if howToReach[currRow][currCol+1] == "" and not investigated[currRow][currCol+1]:
                        queue.append([currRow,currCol+1])
                        howToReach[currRow][currCol+1] = howToReach[currRow][currCol] + "l"
                        
                # check north
                if currRow > 0 and map[currRow-1][currCol] == "X" and searched[currRow-1][currCol] < desperation:
                    pathFound = howToReach[currRow][currCol] + "s"
                    firstAction = keyLookup[pathFound[0]]
                    pathFound = pathFound[1:] # Remove the first instruction; we'll do it seperately and queue the others
                    return firstAction, pathFound
                if currRow > 0 and self.isMapIconPassable(map[currRow-1][currCol]):
                    if howToReach[currRow-1][currCol] == "" and not investigated[currRow-1][currCol]:
                        queue.append([currRow-1,currCol])
                        howToReach[currRow-1][currCol] = howToReach[currRow][currCol] + "k"
                        
                # check west
                if currCol > 0 and map[currRow][currCol-1] == "X" and searched[currRow][currCol-1] < desperation:
                    pathFound = howToReach[currRow][currCol] + "s"
                    firstAction = keyLookup[pathFound[0]]
                    pathFound = pathFound[1:] # Remove the first instruction; we'll do it seperately and queue the others
                    return firstAction, pathFound
                if currCol > 0 and self.isMapIconPassable(map[currRow][currCol-1]):
                    if howToReach[currRow][currCol-1] == "" and not investigated[currRow][currCol-1]:
                        queue.append([currRow,currCol-1])
                        howToReach[currRow][currCol-1] = howToReach[currRow][currCol] + "h"
        # if we're here, there's no suitable target within range
        # what happens next is not this function's responsibility to decide
        # (but it'll probably involve running the function again with a higher desperation value)
        return -1, ""
    
    def markShopOnMap(self, map, row, col):
        if row < 20 and (map[row+1][col] == "." or map[row+1][col] == "-" or map[row+1][col] == "$"):
            map[row+1][col] = "s"
            map = self.markShopOnMap(map, row+1, col)
        if col < 78 and (map[row][col+1] == "." or map[row][col+1] == "-" or map[row][col+1] == "$"):
            map[row][col+1] = "s"
            map = self.markShopOnMap(map, row, col+1)
        if row > 0 and (map[row-1][col] == "." or map[row-1][col] == "-" or map[row-1][col] == "$"):
            map[row-1][col] = "s"
            map = self.markShopOnMap(map, row-1, col)
        if col > 0 and (map[row][col-1] == "." or map[row][col-1] == "-" or map[row][col-1] == "$"):
            map[row][col-1] = "s"
            map = self.markShopOnMap(map, row, col-1)
        return map