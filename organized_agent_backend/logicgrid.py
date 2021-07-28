#!/usr/bin/python

import numpy as np

from bisect import bisect_left
from .items import *
from .narration import CONST_QUIET

def BinarySearch(a, x):
	i = bisect_left(a, x)
	if i != len(a) and a[i] == x:
		return i
	else:
		return -1

class LogicGrid(object):
	def __init__(self, appearances, actuals):
		if len(appearances) != len(actuals):
			# This is a fatal error, so we don't respect CONST_QUIET
			print("Fatal error: Something that spawned a LogicGrid mismatched appearances and actuals.")
			exit(1)	
		# Give appearances and actuals in ascending order, please, so we can binary search!
		self.appearanceIDs = appearances.copy()
		self.possibilityList = []
			# For each appearance, a list of actual objects it could be
		for x in range(len(appearances)):
			self.possibilityList.append(actuals.copy())
		return
	
	def couldBe(self, appearance, actual):
		# Returns true if <appearance> can be <actual>
		appearanceIndex = BinarySearch(self.appearanceIDs, appearance)
		if appearanceIndex == -1:
			if not CONST_QUIET:
				print("Error code 777A: Something that called \"couldBe\" (logicgrid.py) didn't give a valid appearance!")
				print("(Appearance given: ",end="")
				print(appearance,end=")\n")
			return False
		actualIndex = BinarySearch(self.possibilityList[appearanceIndex], actual)
		return (actualIndex != -1)
	def isConfirmedAs(self, appearance, actual):		# Returns true if <appearance> can be <actual>
		appearanceIndex = BinarySearch(self.appearanceIDs, appearance)
		if appearanceIndex == -1:
			if not CONST_QUIET:
				print("Error code 777B: Something that called \"isConfirmedAs\" (logicgrid.py) didn't give a valid appearance!")
				print("(Appearance given: ",end="")
				print(appearance,end=")\n")
			return False
		return (len(self.possibilityList[appearanceIndex]) == 1 and self.possibilityList[appearanceIndex][0] == actual)
	def eliminate(self, appearance, actual):
		appearanceIndex = BinarySearch(self.appearanceIDs, appearance)
		if appearanceIndex == -1:
			if not CONST_QUIET:
				print("Error code 777C: Something that called \"eliminate\" (logicgrid.py) didn't give a valid appearance!")
				print("(Appearance given: ",end="")
				print(appearance,end=")\n")
			return
		actualIndex = BinarySearch(self.possibilityList[appearanceIndex], actual)
		if actualIndex == -1:
			return False # Actual given is either invalid or already ruled out; either way, nothing to do here
		self.possibilityList[appearanceIndex].pop(actualIndex)
		if len(self.possibilityList[appearanceIndex]) == 0:
			# This is a fatal error, so we don't respect CONST_QUIET
			print("Fatal error: No possibilities left for glyph ",end="")
			print(appearance,end="")
			print("! That's not how you logic.")
			exit()
		if len(self.possibilityList[appearanceIndex]) == 1:
			lastPossibility = self.possibilityList[appearanceIndex][0]	
			if not CONST_QUIET:
				print("Matched: \"", end="")
				print(itemNames[itemLookup.index(appearance)], end="")
				print("\" to \"", end="")
				print(itemNames[itemLookup.index(lastPossibility)], end="\"\n")
			self.confirm(appearance, lastPossibility)	
		return True
			
	def confirm(self, appearance, actual):
		appearanceIndex = BinarySearch(self.appearanceIDs, appearance)
		if appearanceIndex == -1:
			if not CONST_QUIET:
				print("Error code 777D: Something that called \"confirm\" (logicgrid.py) didn't give a valid appearance!")
				print("(Appearance given: ",end="")
				print(appearance,end=")\n")
			return
		actualIndex = BinarySearch(self.possibilityList[appearanceIndex], actual)
		if actualIndex == -1:
			# This is a fatal error, so we don't respect CONST_QUIET
			print("Fatal error: Attempted to confirm ruled-out possibility ",end="")
			print(appearance,end="")
			print("=",end="")
			print(actual,end="")
			print("! That's not how you logic.")
			exit(1)			
		self.possibilityList[appearanceIndex] = [actual]
		# This appearance is <actual>, so no other appearance can be <actual>
		eliminatedSomething = False
		for x in self.appearanceIDs:
			if x == appearance:
				continue
			wasEliminated = self.eliminate(x, actual)
			eliminatedSomething = eliminatedSomething or wasEliminated
		if eliminatedSomething and not CONST_QUIET:
			print("Matched: \"", end="")
			print(itemNames[itemLookup.index(appearance)], end="")
			print("\" to \"", end="")
			print(itemNames[itemLookup.index(actual)],end="\"\n")

def isIdentifiable(self, appearance):
	appearanceIndex = BinarySearch(identifiables, appearance)
	return (appearanceIndex != -1)
			

# And now we just include a bunch of useful arrays to use as possibilities and actuals.
# For the following item classes...
	# (cloak, helm, glove, boot, ring, amulet, potion, scroll spellbook, wand)
# ...There is a <class>Appearances and <class>Actuals array
# There's also the "identifiables" array, which is all the glyphs of identifiable objects
# Don't bother scrolling down from here unless you think something's broken.

cloakAppearances = [
	2031,
	2032,
	2033,
	2034
]
helmAppearances = [
	1984,
	1985,
	1986,
	1987
]
gloveAppearances = [
	2042,
	2043,
	2044,
	2045
]
bootAppearances = [
	2049,
	2050,
	2051,
	2052,
	2053,
	2054,
	2055
]
ringAppearances = [
	2056,
	2057,
	2058,
	2059,
	2060,
	2061,
	2062,
	2063,
	2064,
	2065,
	2066,
	2067,
	2068,
	2069,
	2070,
	2071,
	2072,
	2073,
	2074,
	2075,
	2076,
	2077,
	2078,
	2079,
	2080,
	2081,
	2082,
	2083
]
amuletAppearances = [
	2084,
	2085,
	2086,
	2087,
	2088,
	2089,
	2090,
	2091,
	2092
]
potionAppearances = [
	2178,
	2179,
	2180,
	2181,
	2182,
	2183,
	2184,
	2185,
	2186,
	2187,
	2188,
	2189,
	2190,
	2191,
	2192,
	2193,
	2194,
	2195,
	2196,
	2197,
	2198,
	2199,
	2200,
	2201,
	2202
]
scrollAppearances = [
	2204,
	2205,
	2206,
	2207,
	2208,
	2209,
	2210,
	2211,
	2212,
	2213,
	2214,
	2215,
	2216,
	2217,
	2218,
	2219,
	2220,
	2221,
	2222,
	2223,
	2224,
	2225,
	2226,
	2227,
	2228,
	2229,
	2230,
	2231,
	2232,
	2233,
	2234,
	2235,
	2236,
	2237,
	2238,
	2239,
	2240,
	2241,
	2242,
	2243,
	2244
]

spellbookAppearances = [
	2246,
	2247,
	2248,
	2249,
	2250,
	2251,
	2252,
	2253,
	2254,
	2255,
	2256,
	2257,
	2258,
	2259,
	2260,
	2261,
	2262,
	2263,
	2264,
	2265,
	2266,
	2267,
	2268,
	2269,
	2270,
	2271,
	2272,
	2273,
	2274,
	2275,
	2276,
	2277,
	2278,
	2279,
	2280,
	2281,
	2282,
	2283,
	2284,
	2285
]

wandAppearances = [
	2289,
	2290,
	2291,
	2292,
	2293,
	2294,
	2295,
	2296,
	2297,
	2298,
	2299,
	2300,
	2301,
	2302,
	2303,
	2304,
	2305,
	2306,
	2307,
	2308,
	2309,
	2310,
	2311,
	2312,
	2313,
	2314,
	2315
]
cloakActuals = [
	10000,
	10001,
	10002,
	10003
]
helmActuals = [
	10004,
	10005,
	10006,
	10007
]
gloveActuals = [
	10008,
	10009,
	10010,
	10011
]
bootActuals = [
	10012,
	10013,
	10014,
	10015,
	10016,
	10017,
	10018
]
ringActuals = [
	10019,
	10020,
	10021,
	10022,
	10023,
	10024,
	10025,
	10026,
	10027,
	10028,
	10029,
	10030,
	10031,
	10032,
	10033,
	10034,
	10035,
	10036,
	10037,
	10038,
	10039,
	10040,
	10041,
	10042,
	10043,
	10044,
	10045,
	10046
]
amuletActuals = [
	10047,
	10048,
	10049,
	10050,
	10051,
	10052,
	10053,
	10054,
	10055
]
potionActuals = [
	10056,
	10057,
	10058,
	10059,
	10060,
	10061,
	10062,
	10063,
	10064,
	10065,
	10066,
	10067,
	10068,
	10069,
	10070,
	10071,
	10072,
	10073,
	10074, 
	10075, 
	10076,
	10077,
	10078,
	10079,
	10080
]
scrollActuals = [
	10081,
	10082,
	10083,
	10084,
	10085,
	10086,
	10087,
	10088,
	10089,
	10090,
	10091,
	10092,
	10093,
	10094,
	10095,
	10096,
	10097,
	10100,
	10101,
	10102,
	10103,
	# The following 20 IDs are dummies, for the 20 scroll appearances that don't show up in a given episode
	20000,
	20001,
	20002,
	20003,
	20004,
	20005,
	20006,
	20007,
	20008,
	20009,
	20010,
	20011,
	20012,
	20013,
	20014,
	20015,
	20016,
	20017,
	20018,
	20019
]
spellbookActuals = [
	10104,
	10105,
	10106,
	10107,
	10108,
	10109,
	10110, 
	10111,
	10112,
	10113,
	10114,
	10115, 
	10116,
	10117,
	10118,
	10119, 
	10120,
	10121, 
	10122, 
	10123, 
	10124, 
	10125,
	10126,
	10127,
	10128,
	10129,
	10130, 
	10131, 
	10132,
	10133, 
	10134,
	10135,
	10136, 
	10137,
	10138, 
	10139,
	10140,
	10141,
	10142, 
	10143,
]

wandActuals = [
	10144,
	10145,
	10146,
	10147,
	10148,
	10149,
	10150,
	10151,
	10152,
	10153,
	10154,
	10155,
	10156,
	10157,
	10158,
	10159,
	10160,
	10161,
	10162,
	10163,
	10164,
	10165,
	10166,
	10167,
	# Filler for the three wand appearances that don't appear in a given episode
	20000,
	20001,
	20002
]

identifiables = ringAppearances + potionAppearances + scrollAppearances + spellbookAppearances + amuletAppearances + wandAppearances
#identifiables += cloakAppearances + helmAppearances + bootAppearances + cloakAppearances + gloveAppearances