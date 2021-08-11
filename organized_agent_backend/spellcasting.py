#!/usr/bin/python

# Minimum acceptable success chance
CONST_THRESHOLD_CRITICAL = 0.9 # "If I try this and it fails, I'm screwed beyond belief."
CONST_THRESHOLD_IMPORTANT = 0.75 # "I can figure something out if this fails, but please don't fail."
CONST_THRESHOLD_HELPFUL = 0.6 # "I'm rather hoping this works, it'd help."
CONST_THRESHOLD_WHYNOT = 0.3 # "This probably ain't gonna work, but hey, what have I got to lose?"

# Indices in observation["blstats"] where we can check the corresponding stat
CONST_STRENGTH = 3
CONST_INTELLIGENCE = 6
CONST_WISDOM = 7
CONST_CURR_POWER = 14

roleSpellcastingDatabase = {
	"archaeologist" : {
		"base_penalty" : 5,
		"emergency_modifier" : 0,
		"shield_penalty" : 2,
		"mail_penalty" : 10,
		"stat_used" : CONST_INTELLIGENCE,
		"specialty" : "magic mapping"
	},
	"barbarian" : {
		"base_penalty" : 14,
		"emergency_modifier" : 0,
		"shield_penalty" : 0,
		"mail_penalty" : 8,
		"stat_used" : CONST_INTELLIGENCE,
		"specialty" : "magic mapping"
	},
	"caveman" : {
		"base_penalty" : 12,
		"emergency_modifier" : 0,
		"shield_penalty" : 1,
		"mail_penalty" : 8,
		"stat_used" : CONST_INTELLIGENCE,
		"specialty" : "dig"
	},
	"healer" : {
		"base_penalty" : 3,
		"emergency_modifier" : -3,
		"shield_penalty" : 2,
		"mail_penalty" : 10,
		"stat_used" : CONST_WISDOM,
		"specialty" : "cure sickness"
	},
	"knight" : {
		"base_penalty" : 8,
		"emergency_modifier" : -2,
		"shield_penalty" : 0,
		"mail_penalty" : 9,
		"stat_used" : CONST_WISDOM,
		"specialty" : "turn undead"
	},
	"monk" : {
		"base_penalty" : 8,
		"emergency_modifier" : -2,
		"shield_penalty" : 2,
		"mail_penalty" : 20,
		"stat_used" : CONST_WISDOM,
		"specialty" : "restore ability"
	},
	"priest" : {
		"base_penalty" : 3,
		"emergency_modifier" : -2,
		"shield_penalty" : 2,
		"mail_penalty" : 10,
		"stat_used" : CONST_WISDOM,
		"specialty" : "remove curse"
	},
	"ranger" : {
		"base_penalty" : 9,
		"emergency_modifier" : 2,
		"shield_penalty" : 1,
		"mail_penalty" : 10,
		"stat_used" : CONST_INTELLIGENCE,
		"specialty" : "invisibility"
	},
	"rogue" : {
		"base_penalty" : 8,
		"emergency_modifier" : 0,
		"shield_penalty" : 1,
		"mail_penalty" : 9,
		"stat_used" : CONST_INTELLIGENCE,
		"specialty" : "detect treasure"
	},
	"samurai" : {
		"base_penalty" : 10,
		"emergency_modifier" : 0,
		"shield_penalty" : 0,
		"mail_penalty" : 8,
		"stat_used" : CONST_INTELLIGENCE,
		"specialty" : "clairvoyance"
	},
	"tourist" : {
		"base_penalty" : 5,
		"emergency_modifier" : 1,
		"shield_penalty" : 2,
		"mail_penalty" : 10,
		"stat_used" : CONST_INTELLIGENCE,
		"specialty" : "charm monster"
	},
	"valkyrie" : {
		"base_penalty" : 10,
		"emergency_modifier" : -2,
		"shield_penalty" : 0,
		"mail_penalty" : 9,
		"stat_used" : CONST_WISDOM,
		"specialty" : "cone of cold"
	},
	"wizard" : {
		"base_penalty" : 1,
		"emergency_modifier" : 0,
		"shield_penalty" : 3,
		"mail_penalty" : 10,
		"stat_used" : CONST_INTELLIGENCE,
		"specialty" : "magic missile"
	}
}

spellDatabase = {
	"force bolt" : {
		"school" : "attack",
		"level" : 1,
		"is_emergency" : False
	},
	"drain life" : {
		"school" : "attack",
		"level" : 2,
		"is_emergency" : False
	},
	"magic missile" : {
		"school" : "attack",
		"level" : 2,
		"is_emergency" : False
	},
	"cone of cold" : {
		"school" : "attack",
		"level" : 4,
		"is_emergency" : False
	},
	"fireball" : {
		"school" : "attack",
		"level" : 4,
		"is_emergency" : False
	},
	"finger of death" : {
		"school" : "attack",
		"level" : 7,
		"is_emergency" : False
	},
	"protection" : {
		"school" : "clerical",
		"level" : 1,
		"is_emergency" : False
	},
	"create monster" : {
		"school" : "clerical",
		"level" : 2,
		"is_emergency" : False
	},
	"remove curse" : {
		"school" : "clerical",
		"level" : 3,
		"is_emergency" : True
	},
	"create familiar" : {
		"school" : "clerical",
		"level" : 6,
		"is_emergency" : False
	},
	"turn undead" : {
		"school" : "clerical",
		"level" : 6,
		"is_emergency" : False
	},
	"detect monsters" : {
		"school" : "divination",
		"level" : 1,
		"is_emergency" : False
	},
	"light" : {
		"school" : "divination",
		"level" : 1,
		"is_emergency" : False
	},
	"detect food" : {
		"school" : "divination",
		"level" : 2,
		"is_emergency" : False
	},
	"clairvoyance" : {
		"school" : "divination",
		"level" : 3,
		"is_emergency" : False
	},
	"detect unseen" : {
		"school" : "divination",
		"level" : 3,
		"is_emergency" : False
	},
	"identify" : {
		"school" : "divination",
		"level" : 3,
		"is_emergency" : False
	},
	"detect treasure" : {
		"school" : "divination",
		"level" : 4,
		"is_emergency" : False
	},
	"magic mapping" : {
		"school" : "divination",
		"level" : 5,
		"is_emergency" : False
	},
	"sleep" : {
		"school" : "enchantment",
		"level" : 1,
		"is_emergency" : False
	},
	"confuse monster" : {
		"school" : "enchantment",
		"level" : 2,
		"is_emergency" : False
	},
	"slow monster" : {
		"school" : "enchantment",
		"level" : 2,
		"is_emergency" : False
	},
	"cause fear" : {
		"school" : "enchantment",
		"level" : 3,
		"is_emergency" : False
	},
	"charm monster" : {
		"school" : "enchantment",
		"level" : 3,
		"is_emergency" : False
	},
	"jumping" : {
		"school" : "escape",
		"level" : 1,
		"is_emergency" : False
	},
	"haste self" : {
		"school" : "escape",
		"level" : 3,
		"is_emergency" : False
	},
	"invisibility" : {
		"school" : "escape",
		"level" : 4,
		"is_emergency" : False
	},
	"levitation" : {
		"school" : "escape",
		"level" : 4,
		"is_emergency" : False
	},
	"teleport away" : {
		"school" : "escape",
		"level" : 6,
		"is_emergency" : False
	},
	"healing" : {
		"school" : "healing",
		"level" : 1,
		"is_emergency" : True
	},
	"cure blindness" : {
		"school" : "healing",
		"level" : 2,
		"is_emergency" : True
	},
	"cure sickness" : {
		"school" : "healing",
		"level" : 3,
		"is_emergency" : True
	},
	"extra healing" : {
		"school" : "healing",
		"level" : 3,
		"is_emergency" : True
	},
	"stone to flesh" : {
		"school" : "healing",
		"level" : 3,
		"is_emergency" : False
	},
	"restore ability" : {
		"school" : "healing",
		"level" : 4,
		"is_emergency" : True
	},
	"knock" : {
		"school" : "matter",
		"level" : 1,
		"is_emergency" : False
	},
	"wizard lock" : {
		"school" : "matter",
		"level" : 2,
		"is_emergency" : False
	},
	"dig" : {
		"school" : "matter",
		"level" : 5,
		"is_emergency" : False
	},
	"polymorph" : {
		"school" : "matter",
		"level" : 6,
		"is_emergency" : False
	},
	"cancellation" : {
		"school" : "matter",
		"level" : 7,
		"is_emergency" : False
	}
}