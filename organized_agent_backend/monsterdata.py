#!/usr/bin/python

monsterDatabase = [
	# List monsters in glyph ID order
	{
		"name" : "black dragon",
		"dmg" : [13.5, 2.5, 2.5], # expected value of damage for each attack seperately
		"difficulty" : 20,
		"base_level" : 15,
		"speed" : 9,
		"base_ac" : -1,
		"base_mr" : 20,
		"size" : 7, # see https://nethackwiki.com/wiki/Physical_size
		"resistances" : ["disintegration"],
		"tags" : ["can_fly","no_hands","thick_hide","see_invisible","strong","lays_eggs"]
	}
	
]