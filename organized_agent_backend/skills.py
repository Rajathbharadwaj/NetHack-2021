#!/usr/bin/python

from .inventory import *
from .utilities import *
from .narration import CONST_QUIET

CONST_NUM_SKILLS = 39
CONST_FIRST_WEAPON = 4
CONST_LAST_WEAPON = 31

skillNames = [
	"bare hands", # 0
	"two weapon combat", # 1
	"riding", # 2
	"martial arts", # 3
	"dagger", # 4
	"knife", # 5
	"axe", # 6
	"pick-axe", # 7
	"short sword", # 8
	"broadsword", # 9
	"long sword", # 10
	"two-handed sword", # 11
	"scimitar", # 12
	"saber", # 13
	"club", # 14
	"mace", # 15
	"morning star", # 16
	"flail", # 17
	"hammer", # 18
	"quarterstaff", # 19
	"polearms", # 20
	"spear", # 21
	"trident", # 22
	"lance", # 23
	"bow", # 24
	"sling", # 25
	"crossbow", # 26
	"dart", # 27
	"shuriken", # 28
	"boomerang", # 29
	"whip", # 30
	"unicorn horn", # 31
	"attack magic", # 32
	"healing magic", # 33
	"divination magic", # 34
	"enchantment magic", # 35
	"clerical magic", # 36
	"escape magic", # 37
	"matter magic" # 38
]

weaponGlyphs = [
	[],
	[],
	[],
	[],
	[ # daggers
		1923,
		1924,
		1925,
		1926,
		1927
	],
	[ # knives
		1928,
		1929,
		1930,
		1931,
		1932
	],
	[ # axes
		1933,
		1934
	],
	[ # pick-axes
		1956,
		2140
	],
	[ # short swords
		1935,
		1936,
		1937,
		1938
	],
	[ # broadswords
		1941,
		1942,
		1947
	],
	[ # long swords
		1943,
		1945
	],
	[ # two-handed swords
		1944,
		1946
	],
	[ # scimitars
		1939
	],
	[ # sabers
		1940
	],
	[ # clubs
		1965,
		1968
	],
	[ # maces
		1962
	],
	[ # morning stars
		1963
	],
	[ # flails
		1969,
		2141
	],
	[ # hammers
		1964
	],
	[ # quarterstaves
		1967
	],
	[ # polearms
		1948,
		1949,
		1950,
		1951,
		1953,
		1954,
		1955,
		1957,
		1958,
		1959,
		1960,
		1961
	],
	[ # spears
		1916,
		1917,
		1918,
		1919,
		1920,
		1921
	],
	[ # tridents
		1922
	],
	[ # lances
		1952
	],
	[ # bows
		1971,
		1972,
		1973,
		1974
	],
	[ # slings
		1975
	],
	[ # crossbows
		1976
	],
	[ # darts
		1913
	],
	[ # shuriken
		1914
	],
	[ # boomerangs
		1915
	],
	[ # whips
		1966,
		1970
	],
	[ # unicorn horns
		2142
	]
]



class Skillset(object):
	def __init__(self, state, observations, role):
		self.skillLevels = [0] * CONST_NUM_SKILLS
		self.readyToImprove = [False] * CONST_NUM_SKILLS
		self.upgradeLog = []
		self.skillSlotsSpent = 0
		if(role == "archaeologist"):
			self.skillLevels[30] = 1 # whip
			self.skillLevels[7] = 1 # pickaxe
			return
		if(role == "barbarian"):
			self.skillLevels[6] = 1 # axe
			self.skillLevels[0] = 1 # bare hands
			if len(searchInventory(state, observations, weaponGlyphs[8])[0]) > 0:
				self.skillLevels[8] = 1 # short sword
				return
			if len(searchInventory(state, observations, weaponGlyphs[11])[0]) > 0:
				self.skillLevels[11] = 1 # two-handed sword
				return
			print("FATAL ERROR: Agent is supposedly a barbarian but doesn't start with a sword?")
			exit(1)
		if(role == "caveman"):
			self.skillLevels[14] = 1 # club
			self.skillLevels[25] = 1 # sling
			self.skillLevels[0] = 1 # bare hands
			return
		if(role == "healer"):
			self.skillLevels[5] = 1 # knife
			self.skillLevels[33] = 1 # healing magic
			return
		if(role == "knight"):
			self.skillLevels[10] = 1 # long sword
			self.skillLevels[23] = 1 # lance
			self.skillLevels[2] = 1 # riding
			return
		if(role == "monk"):
			self.skillLevels[3] = 1 # martial arts
			self.skillLevels[33] = 1 # healing magic
			return
		if(role == "priest"):
			self.skillLevels[15] = 1 # mace
			self.skillLevels[36] = 1 # clerical magic
			return
		if(role == "rogue"):
			self.skillLevels[8] = 1 # short sword
			self.skillLevels[4] = 1 # dagger
			return
		if(role == "ranger"):
			self.skillLevels[4] = 1 # dagger
			if len(searchInventory(state, observations, weaponGlyphs[24])[0]) > 0:
				self.skillLevels[24] = 1 # short sword
				return
			if len(searchInventory(state, observations, weaponGlyphs[26])[0]) > 0:
				self.skillLevels[26] = 1 # two-handed sword
				return
			print("FATAL ERROR: Agent is supposedly a ranger but doesn't start with a launcher?")
			exit(1)
			return
		if(role == "samurai"):
			self.skillLevels[10] = 1 # long sword
			self.skillLevels[8] = 1 # short sword
			self.skillLevels[24] = 1 # bow
			self.skillLevels[3] = 1 # martial arts
			return
		if(role == "tourist"):
			self.skillLevels[27] = 1 # dart
			return
		if(role == "valkyrie"):
			self.skillLevels[10] = 1 # long sword
			self.skillLevels[4] = 1 # dagger
			return
		if(role == "wizard"):
			self.skillLevels[19] = 1 # quarterstaff
			self.skillLevels[32] = 1 # attack magic
			self.skillLevels[35] = 1 # enchantment magic
			return
		print("FATAL ERROR: Attempted to initialize skillset for unrecognized role \"" + role + "\"")
		exit(1)
	def readyToFight(self, state, observations):
		# "You feel more confident in your fighting skills."
		# We're ready to enhance our skill in either bare hands combat, two-weaponing, or riding. But which?
		# If we have no wielded weapon, it's bare hands combat. (which some roles know as "martial arts")
		# If we have two wielded weapons, it's two-weaponing.
		# If we're riding, it's riding.
		
		# Except for one little problem.
		# We could be riding with no wielded weapon, or with two weapons,
		# in which case it could be either riding or the other appropriate skill.
		# uhhhhhhhhhhhhhh
		# I'm not sure how to determine for sure which it is.
		# Maybe we could remember if we spent the last step fighting or not,
		# but even that's not foolproof. (We sometimes walk into monsters to fight them)
		
		# For right now I'll just give riding the lowest priority, because we don't actually ever ride yet.
		# Still, TODO, because it's kinda bad if we guess wrong on this
		
		wielded = len(whatIsWielded(state, observations)[0])
		if wielded == 0 and not self.readyToImprove[0] and not self.readyToImprove[3]:
			if not CONST_QUIET:
				print("Agent's nice and practiced at boxing.")
			if state.role == "monk" or state.role == "samurai":
				self.readyToImprove[3] = True
			else:
				self.readyToImprove[0] = True
			return
		
		if wielded == 2 and not self.readyToImprove[1]:
			if not CONST_QUIET:
				print("Agent's nice and practiced at dual wielding.")
			self.readyToImprove[1] = True
			return
		
		if readHeroStatus(observations, 12) and not self.readyToImprove[2]:
			if not CONST_QUIET:
				print("Agent's nice and practiced at monsterback.")
			self.readyToImprove[2] = True
			return
		
		# If we're here, we probably guessed wrong before about which skill we became ready to enhance.
		# Might as well spit out the details of what happened.
		print("FATAL ERROR: Agent is told its fighting skills are ready to enhance, but that shouldn't be possible.")
		print("Wielded: ",end="")
		print(whatIsWielded(state, observations)[0])
		if readHeroStatus(observations, 12):
			print("Agent was riding.")
		if self.readyToImprove[0] or self.readyToImprove[3]:
			print("Agent was already ready to improve at boxing.")
		if self.readyToImprove[1]:
			print("Agent was already ready to improve at dual wielding.")
		if self.readyToImprove[2]:
			print("Agent was already ready to improve at riding.")
		exit(1)
	
	def readyToWield(self, state, observations):
		# "You feel more confident in your weapon skills."
		# Let's figure out which weapon that was.
		wieldList = whatIsWielded(state, observations)[1]
		if len(wieldList) != 1:
			print("FATAL ERROR: Agent is told its weapon skills are ready to enhance, but that shouldn't be possible.")
			print("Wielded: ",end="")
			print(wieldList)
			print("In this situation, the agent should be training its fighting skills, not its weapon skills.")
			exit(1)
		wielded = wieldList[0]
		for x in range(len(weaponGlyphs)):
			weaponClass = weaponGlyphs[x]
			if wielded in weaponClass:
				if self.readyToImprove[x]:
					print("FATAL ERROR: Agent is told its weapon skills are ready to enhance, but that shouldn't be possible.")
					print("Wielded: ",end="")
					print(wieldList)
					print("But the agent was already ready to enhance its skill with the ",end="")
					print(skillNames[x],end="")
					print(", so it makes no sense...")
					exit(1)
				print("Agent is nice and practiced with the ",end="")
				print(skillNames[x],end="")
				print(".")
				self.readyToImprove[x] = True
				return
			
		print("FATAL ERROR: Agent is told its weapon skills are ready to enhance, but that shouldn't be possible.")
		print("Wielded: ",end="")
		print(wieldList)
		print("That's... not any kind of weapon. How are we able to become skilled in wielding that?")
		exit(1)

	def readyToCast(self, state, observations):
		# TODO (give gamestate.py a variable to keep track of the last spell school invoked, then come back here and write this function.)
		return
	
	def readyToBeDangerous(self, state, observations):
		# "You feel you could be more dangerous!"
		# Whatever skill we #Enhanced last can be enhanced again!
		if len(self.upgradeLog) == 0:
			print("FATAL ERROR: Agent is told it can upgrade its skills again, but that shouldn't be possible.")
			print("It never enhanced anything in the first place! How can it enhance 'again' if there was no...")
			print("Ah, forget it. Exiting in shame.")
			exit(1)
		lastUpgraded = self.upgradeLog[-1]
		if self.readyToImprove[lastUpgraded]:
			print("FATAL ERROR: Agent failed to unmark the skill it just enhanced as 'ready to improve'.")
			print("Go to skills.py and fix the checkSkills function.")
			print("Oh, and in case it matters, the skill the agent upgraded was: ",end="")
			print(skillNames[lastUpgraded])
			exit(1)
		self.readyToImprove[lastUpgraded] = True
		return
	
	def checkUpgradeCost(self, skillID):
		# (in skill slots)
		if self.skillLevels[skillID] < 0:
			print("FATAL ERROR: ",end="")
			print(skillNames[skillID],end="")
			print(" skill is listed as having negative level? What even?")
			exit(1)
		prevLevel = self.skillLevels[skillID]
		if skillID >= CONST_FIRST_WEAPON and skillID <= CONST_LAST_WEAPON:
			if prevLevel > 3:
				print("FATAL ERROR: ",end="")
				print(skillNames[skillID],end="")
				print(" skill is listed as having an impossibly high level. (",end="")
				print(self.skillLevels[skillID],end="")
				print(")")
				exit(1)
			if prevLevel == 3:
				return 999 # Skill can't possibly be enhanced any more
			return prevLevel + 1 # Upgrading from 0 costs 1, from 1 costs 2, and from 2 costs 3
		# if we're here we've been asked about a non-weapon skill
		if prevLevel <= 1:
			return 1
		if prevLevel <= 3:
			return 2
		if prevLevel == 4:
			return 3
		if prevLevel == 5:
			return 999 # Skill can't possibly be enhanced any more
		
		print("FATAL ERROR: ",end="")
		print(skillNames[skillID],end="")
		print(" skill is listed as having an impossibly high level. (",end="")
		print(self.skillLevels[skillID],end="")
		print(")")
		exit(1)
		
def checkSkills(state, observations):
	readySkills = []
	skillSlots = state.lastKnownLOVE - 1 - state.skills.skillSlotsSpent # Crowning will be accounted for... someday
	while skillSlots < 0:
		if len(state.skills.upgradeLog) == 0:
			print("FATAL ERROR: Agent lost a skill, but already didn't have any skills left.")
			print("LOVE:",state.lastKnownLOVE)
			exit(1)
		skillLost = state.skills.upgradeLog[-1]
		state.skills.skillLevels[skillLost] -= 1
		state.skills.readyToImprove[skillLost] = True # in this scenario it's actually okay if it was already true
		state.skills.upgradeLog = state.skills.upgradeLog[:-1] # pop skill from upgrade log
		state.skills.skillSlotsSpent -= state.skills.checkUpgradeCost(skillLost)
		skillSlots += state.skills.checkUpgradeCost(skillLost)
		print("Regrettably,", skillNames[skillLost],"skill downgraded due to level drain...")
	
	for x in range(len(state.skills.readyToImprove)):
		if state.skills.readyToImprove[x] and state.skills.checkUpgradeCost(x) <= skillSlots:
			readySkills.append(x)
	if len(readySkills) > 0:
		skillOfChoice = considerImproving(state, observations, readySkills)
		if skillOfChoice == -1:
			return -1
		else:
			if not CONST_QUIET:
				print("Agent's " + skillNames[readySkills[skillOfChoice]] + " skill has been upgraded!")
			state.skills.skillSlotsSpent += state.skills.checkUpgradeCost(readySkills[skillOfChoice])
			state.skills.readyToImprove[readySkills[skillOfChoice]] = False
			state.skills.skillLevels[readySkills[skillOfChoice]] += 1
			state.queue = [slotLookup[skillOfChoice]] # "Enhance what?" -> skillOfChoice
			return 38 # Enhance
	return -1

def considerImproving(state, observations, readySkills):
	# TODO: Add more logic for the various classes. For now we just enhance whatever we can
	# Return the index (in readySkills, not skillNames) of the skill we want to improve
	# Or, if we'd rather save our skill slots, return -1 to improve nothing
	# By the way, note that readySkills is guaranteed to have at least 1 element
	return 0

# TODO: Have behaviors.py include checkSkills in its agenda, and then start debugging, because there's no way there aren't bugs