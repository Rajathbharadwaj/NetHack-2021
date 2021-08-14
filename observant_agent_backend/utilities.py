#!/usr/bin/python

# observant_agent

from .agent_config import *

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
	"$" : 112,
	"+" : 97,
	"-" : 98,
	" " : 99,
	"*" : 76,
	"#" : 20,
	"?" : 21,
	"\n" : 19 # represents enter
}

def parse(str):
	# The observations give us text in the form of ascii numbers
	# This turns those ascii numbers 
	return bytes(str).decode('ascii').replace('\0','')

def readHeroPos(observations):
	# Returns hero row, hero col
	return observations["blstats"][1], observations["blstats"][0]

def readCursorPos(observations):
	# Returns cursor row, cursor col (relative to the game grid, not to the whole screen)
	return observations["tty_cursor"][0]-1, observations["tty_cursor"][1]

def readTurn(observations):
	return observations["blstats"][20]

def readMessage(observations):
	return parse(observations["message"])

def readDungeonNum(observations):
	return observations["blstats"][23]

def readDungeonLevel(observations):
	# Subtract one so it lines up with our zero-indexed arrays
	return observations["blstats"][24]-1

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
	
	output = []
	if observations != []:
		heroRow, heroCol = readHeroPos(observations)
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
	
	return output