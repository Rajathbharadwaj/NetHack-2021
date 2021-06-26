#!/usr/bin/python

compass = {
	"N" : "k",
	"NE" : "u",
	"E" : "l",
	"SE" : "n",
	"S" : "j",
	"SW" : "b",
	"W" : "h",
	"NW" : "y"
}

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
	"}" : 19, # represents enter ("}" serves no inherent purpose in nethack)
	"{" : -1 # special character; represents an open slot in the queue
}