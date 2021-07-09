#!/usr/bin/python

# These lists contain glyph numbers that correspond to items that have a common usage

lockpicks = [2103, 2104]

blinds = [2114, 2115]

permafood = [1299, 2147, 2148, 2149, 2150, 2151, 2158, 2159, 2160, 2161, 2162, 2163, 2164, 2166, 2168, 2170, 2172, 2173, 2174, 2175, 2176, 2177]

worthTaking = [1299, 2103, 2104, 2114, 2115, 2147, 2148, 2149, 2150, 2151, 2158, 2159, 2160, 2161, 2162, 2163, 2164, 2166, 2168, 2170, 2172, 2173, 2174, 2175, 2176, 2177]

# These are two parallel arrays indexing the glyph IDs of every item, and giving their visible name.
# This way, the agent can look in this table to figure out what's what, when it sees "you see here a <thing>"
# And I don't have to hard-code it to recognize every single one of the >400 items in the game individually.

# ...I will probably have to program it to *respond* to (almost) every single one of the >400 items in the game.
# For every beatitude plus a seperate case for unknown beatitude.
# I
# am not entirely looking forward to that. It's an awful big ask for just one person.
# But for now, here are the arrays.

itemNames = [
	"pear", # a bunch of stuff has "pear" in its name so this is going straight to the front to avoid confusion
	"strange object",
	"runed arrow",
	"crude arrow",
	"silver arrow",
	"bamboo arrow",
	"arrow",
	"crossbow bolt",
	"dart",
	"throwing star",
	"boomerang",
	"spear",
	"runed spear",
	"crude spear",
	"stout spear",
	"silver spear",
	"throwing spear",
	"trident",
	"dagger",
	"runed dagger",
	"crude dagger",
	"silver dagger",
	"athame",
	"scalpel",
	"knife",
	"stiletto",
	"worm tooth",
	"crysknife",
	"axe",
	"double-headed axe",
	"short sword",
	"runed short sword",
	"crude short sword",
	"broad short sword",
	"curved sword",
	"silver saber",
	"broadsword",
	"runed broadsword",
	"long sword",
	"two-handed sword",
	"samurai sword",
	"long samurai sword",
	"runed broadsword",
	"vulgar polearm",
	"hilted polearm",
	"forked polearm",
	"single-edged polearm",
	"lance",
	"angled poleaxe",
	"long poleaxe",
	"pole cleaver",
	"broad pick",
	"pole sickle",
	"pruning hook",
	"hooked polearm",
	"pronged polearm",
	"beaked polearm",
	"mace",
	"morning star",
	"war hammer",
	"club",
	"rubber hose",
	"staff",
	"thonged club",
	"flail",
	"bullwhip",
	"bow",
	"runed bow",
	"crude bow",
	"long bow",
	"sling",
	"crossbow",
	"leather hat",
	"iron skull cap",
	"hard hat",
	"fedora",
	"conical hat",
	"conical hat",
	"dented pot",
	"plumed helmet",
	"etched helmet",
	"crested helmet",
	"visored helmet",
	"gray dragon scale mail",
	"silver dragon scale mail",
	"red dragon scale mail",
	"white dragon scale mail",
	"orange dragon scale mail",
	"black dragon scale mail",
	"blue dragon scale mail",
	"green dragon scale mail",
	"yellow dragon scale mail",
	"gray dragon scales",
	"silver dragon scales",
	"red dragon scales",
	"white dragon scales",
	"orange dragon scales",
	"black dragon scales",
	"blue dragon scales",
	"green dragon scales",
	"yellow dragon scales",
	"plate mail",
	"crystal plate mail",
	"bronze plate mail",
	"splint mail",
	"banded mail",
	"dwarvish mithril-coat",
	"elven mithril-coat",
	"chain mail",
	"crude chain mail",
	"scale mail",
	"studded leather armor",
	"ring mail",
	"crude ring mail",
	"leather armor",
	"leather jacket",
	"Hawaiian shirt",
	"T-shirt",
	"mummy wrapping",
	"faded pall",
	"coarse mantelet",
	"hooded cloak",
	"slippery cloak",
	"robe",
	"apron",
	"leather cloak",
	"tattered cape",
	"opera cloak",
	"ornamental cope",
	"piece of cloth",
	"small shield",
	"blue and green shield",
	"white-handed shield",
	"red-eyed shield",
	"large shield",
	"large round shield",
	"polished silver shield",
	"old gloves",
	"padded gloves",
	"riding gloves",
	"fencing gloves",
	"walking shoes",
	"hard shoes",
	"jackboots",
	"combat boots",
	"jungle boots",
	"hiking boots",
	"mud boots",
	"buckled boots",
	"riding boots",
	"snow boots",
	"wooden ring",
	"granite ring",
	"opal ring",
	"clay ring",
	"coral ring",
	"black onyx ring",
	"moonstone ring",
	"tiger eye ring",
	"jade ring",
	"bronze ring",
	"agate ring",
	"topaz ring",
	"sapphire ring",
	"ruby ring",
	"diamond ring",
	"pearl ring",
	"iron ring",
	"brass ring",
	"copper ring",
	"twisted ring",
	"steel ring",
	"silver ring",
	"gold ring",
	"ivory ring",
	"emerald ring",
	"wire ring",
	"engagement ring",
	"shiny ring",
	"circular amulet",
	"spherical amulet",
	"oval amulet",
	"triangular amulet",
	"pyramidal amulet",
	"square amulet",
	"concave amulet",
	"hexagonal amulet",
	"octagonal amulet",
	"Amulet of Yendor amulet",
	"Amulet of Yendor amulet",
	"large box",
	"chest",
	"ice box",
	"bag",
	"bag",
	"bag",
	"bag",
	"key",
	"lock pick",
	"credit card",
	"candle",
	"candle",
	"brass lantern",
	"lamp",
	"lamp",
	"expensive camera",
	"looking glass",
	"glass orb",
	"lenses",
	"blindfold",
	"towel",
	"saddle",
	"leash",
	"stethoscope",
	"tin",
	"tinning kit",
	"tin opener",
	"can of grease",
	"figurine",
	"magic marker",
	"land mine",
	"beartrap",
	"whistle",
	"whistle",
	"flute",
	"flute",
	"horn",
	"horn",
	"horn",
	"horn",
	"harp",
	"harp",
	"bell",
	"bugle",
	"drum",
	"drum",
	"pick-axe",
	"iron hook",
	"unicorn horn",
	"candelabrum",
	"silver bell",
	"tripe ration",
	"corpse",
	"egg",
	"meatball",
	"meat stick",
	"huge chunk of meat",
	"meat ring",
	"glob of gray ooze",
	"glob of brown pudding",
	"glob of green slime",
	"glob of black pudding",
	"kelp frond",
	"eucalyptus leaf",
	"apple",
	"orange",
	"melon",
	"banana",
	"carrot",
	"sprig of wolfsbane",
	"clove of garlic",
	"slime mold",
	"lump of royal jelly",
	"cream pie",
	"candy bar",
	"fortune cookie",
	"pancake",
	"lembas wafer",
	"cram ration",
	"food ration",
	"K-ration",
	"C-ration",
	"ruby potion",
	"pink potion",
	"orange potion",
	"yellow potion",
	"emerald potion",
	"dark green potion",
	"cyan potion",
	"sky blue potion",
	"brilliant blue potion",
	"magenta potion",
	"purple-red potion",
	"puce potion",
	"milky potion",
	"swirly potion",
	"bubbly potion",
	"smoky potion",
	"cloudy potion",
	"effervescent potion",
	"black potion",
	"golden potion",
	"brown potion",
	"fizzy potion",
	"dark potion",
	"white potion",
	"murky potion",
	"clear potion",
	"ZELGO MER",
	"JUYED AWK YACC",
	"NR 9",
	"XIXAXA XOXAXA XUXAXA",
	"PRATYAVAYAH",
	"DAIYEN FOOELS",
	"LEP GEX VEN ZEA",
	"PRIRUTSENIE",
	"ELBIB YLOH",
	"VERR YED HORRE",
	"VENZAR BORGAVVE",
	"THARR",
	"YUM YUM",
	"KERNOD WEL",
	"ELAM EBOW",
	"DUAM XNAHT",
	"ANDOVA BEGARIN",
	"KIRJE",
	"VE FORBRYDERNE",
	"HACKEM MUCHE",
	"VELOX NEB",
	"FOOBIE BLETCH",
	"TEMOV",
	"GARVEN DEH",
	"READ ME",
	"ETAOIN SHRDLU",
	"LOREM IPSUM",
	"FNORD",
	"KO BATE",
	"ABRA KA DABRA",
	"ASHPD SODALG",
	"ZLORFIK",
	"GNIK SISI VLE",
	"HAPAX LEGOMENON",
	"EIRIS SAZUN IDISI",
	"PHOL ENDE WODAN",
	"GHOTI",
	"MAPIRO MAHAMA DIROMAT",
	"VAS CORP BET MANI",
	"XOR OTA",
	"STRC PRST SKRZ KRK",
	"unlabeled",
	"parchment spellbook",
	"vellum spellbook",
	"ragged spellbook",
	"dog eared spellbook",
	"mottled spellbook",
	"stained spellbook",
	"cloth spellbook",
	"leathery spellbook",
	"white spellbook",
	"pink spellbook",
	"red spellbook",
	"orange spellbook",
	"yellow spellbook",
	"velvet spellbook",
	"light green spellbook",
	"dark green spellbook",
	"turquoise spellbook",
	"cyan spellbook",
	"light blue spellbook",
	"dark blue spellbook",
	"indigo spellbook",
	"magenta spellbook",
	"purple spellbook",
	"violet spellbook",
	"tan spellbook",
	"plaid spellbook",
	"light brown spellbook",
	"dark brown spellbook",
	"gray spellbook",
	"wrinkled spellbook",
	"dusty spellbook",
	"bronze spellbook",
	"copper spellbook",
	"silver spellbook",
	"gold spellbook",
	"glittering spellbook",
	"shining spellbook",
	"dull spellbook",
	"thin spellbook",
	"thick spellbook",
	"plain spellbook",
	"paperback spellbook",
	"papyrus spellbook",
	"glass wand",
	"balsa wand",
	"crystal wand",
	"maple wand",
	"pine wand",
	"oak wand",
	"ebony wand",
	"marble wand",
	"tin wand",
	"brass wand",
	"copper wand",
	"silver wand",
	"platinum wand",
	"iridium wand",
	"zinc wand",
	"aluminum wand",
	"uranium wand",
	"iron wand",
	"steel wand",
	"hexagonal wand",
	"short wand",
	"runed wand",
	"long wand",
	"curved wand",
	"forked wand",
	"spiked wand",
	"jeweled wand",
	"gold piece",
	"white gem",
	"white gem",
	"red gem",
	"orange gem",
	"blue gem",
	"black gem",
	"green stone",
	"green stone",
	"yellow gem",
	"green stone",
	"yellowish brown gem",
	"yellowish brown gem",
	"black gem",
	"white gem",
	"yellow gem",
	"red gem",
	"violet gem",
	"red gem",
	"violet gem",
	"black gem",
	"orange gem",
	"green stone",
	"white gem",
	"blue gem",
	"red gem",
	"yellowish brown gem",
	"orange gem",
	"yellow gem",
	"black gem",
	"green stone",
	"violet gem",
	"gray stone",
	"gray stone",
	"gray stone",
	"gray stone",
	"rock gem",
	"boulder",
	"statue",
	"heavy iron ball",
	"iron chain",
	"splash of venom",
	"splash of venom",
	# Now for corpses.
	# Not all of these are corpses you'll ever find but that's okay
	"giant ant corpse",
	"killer bee corpse",
	"soldier ant corpse",
	"fire ant corpse",
	"giant beetle corpse",
	"queen bee corpse",
	"acid blob corpse",
	"quivering blob corpse",
	"gelatinous cube corpse",
	"chickatrice corpse",
	"cockatrice corpse",
	"pyrolisk corpse",
	"jackal corpse",
	"fox corpse",
	"coyote corpse",
	"werejackal corpse",
	"little dog corpse",
	"dingo corpse",
	"dog corpse",
	"large dog corpse",
	"wolf corpse",
	"werewolf corpse",
	"winter wolf cub corpse",
	"warg corpse",
	"winter wolf corpse",
	"hell hound pup corpse",
	"hell hound corpse",
	"gas spore corpse",
	"floating eye corpse",
	"freezing sphere corpse",
	"flaming sphere corpse",
	"shocking sphere corpse",
	"kitten corpse",
	"housecat corpse",
	"jaguar corpse",
	"lynx corpse",
	"panther corpse",
	"large cat corpse",
	"tiger corpse",
	"gremlin corpse",
	"gargoyle corpse",
	"winged gargoyle corpse",
	"hobbit corpse",
	"dwarf corpse",
	"bugbear corpse",
	"dwarf lord corpse",
	"dwarf king corpse",
	"mind flayer corpse",
	"master mind flayer corpse",
	"manes corpse",
	"homunculus corpse",
	"imp corpse",
	"lemure corpse",
	"quasit corpse",
	"tengu corpse",
	"blue jelly corpse",
	"spotted jelly corpse",
	"ochre jelly corpse",
	"kobold corpse",
	"large kobold corpse",
	"kobold lord corpse",
	"kobold shaman corpse",
	"leprechaun corpse",
	"small mimic corpse",
	"large mimic corpse",
	"giant mimic corpse",
	"wood nymph corpse",
	"water nymph corpse",
	"mountain nymph corpse",
	"goblin corpse",
	"hobgoblin corpse",
	"orc corpse",
	"hill orc corpse",
	"Mordor orc corpse",
	"Uruk-hai corpse",
	"orc shaman corpse",
	"orc-captain corpse",
	"rock piercer corpse",
	"iron piercer corpse",
	"glass piercer corpse",
	"rothe corpse",
	"mumak corpse",
	"leocrotta corpse",
	"wumpus corpse",
	"titanothere corpse",
	"baluchitherium corpse",
	"mastodon corpse",
	"sewer rat corpse",
	"giant rat corpse",
	"rabid rat corpse",
	"wererat corpse",
	"rock mole corpse",
	"woodchuck corpse",
	"cave spider corpse",
	"centipede corpse",
	"giant spider corpse",
	"scorpion corpse",
	"lurker above corpse",
	"trapper corpse",
	"pony corpse",
	"white unicorn corpse",
	"gray unicorn corpse",
	"black unicorn corpse",
	"horse corpse",
	"warhorse corpse",
	"fog cloud corpse",
	"dust vortex corpse",
	"ice vortex corpse",
	"energy vortex corpse",
	"steam vortex corpse",
	"fire vortex corpse",
	"baby long worm corpse",
	"baby purple worm corpse",
	"long worm corpse",
	"purple worm corpse",
	"grid bug corpse",
	"xan corpse",
	"yellow light corpse",
	"black light corpse",
	"zruty corpse",
	"couatl corpse",
	"Aleax corpse",
	"Angel corpse",
	"ki-rin corpse",
	"Archon corpse",
	"bat corpse",
	"giant bat corpse",
	"raven corpse",
	"vampire bat corpse",
	"plains centaur corpse",
	"forest centaur corpse",
	"mountain centaur corpse",
	"baby gray dragon corpse",
	"baby silver dragon corpse",
	"baby red dragon corpse",
	"baby white dragon corpse",
	"baby orange dragon corpse",
	"baby black dragon corpse",
	"baby blue dragon corpse",
	"baby green dragon corpse",
	"baby yellow dragon corpse",
	"gray dragon corpse",
	"silver dragon corpse",
	"red dragon corpse",
	"white dragon corpse",
	"orange dragon corpse",
	"black dragon corpse",
	"blue dragon corpse",
	"green dragon corpse",
	"yellow dragon corpse",
	"stalker corpse",
	"air elemental corpse",
	"fire elemental corpse",
	"earth elemental corpse",
	"water elemental corpse",
	"lichen corpse",
	"brown mold corpse",
	"yellow mold corpse",
	"green mold corpse",
	"red mold corpse",
	"shrieker corpse",
	"violet fungus corpse",
	"gnome corpse",
	"gnome lord corpse",
	"gnomish wizard corpse",
	"gnome king corpse",
	"giant corpse",
	"stone giant corpse",
	"hill giant corpse",
	"fire giant corpse",
	"frost giant corpse",
	"ettin corpse",
	"storm giant corpse",
	"titan corpse",
	"minotaur corpse",
	"jabberwock corpse",
	"Keystone Kop corpse",
	"Kop Sergeant corpse",
	"Kop Lieutenant corpse",
	"Kop Kaptain corpse",
	"lich corpse",
	"demilich corpse",
	"master lich corpse",
	"arch-lich corpse",
	"kobold mummy corpse",
	"gnome mummy corpse",
	"orc mummy corpse",
	"dwarf mummy corpse",
	"elf mummy corpse",
	"human mummy corpse",
	"ettin mummy corpse",
	"giant mummy corpse",
	"red naga hatchling corpse",
	"black naga hatchling corpse",
	"golden naga hatchling corpse",
	"guardian naga hatchling corpse",
	"red naga corpse",
	"black naga corpse",
	"golden naga corpse",
	"guardian naga corpse",
	"ogre corpse",
	"ogre lord corpse",
	"ogre king corpse",
	"gray ooze corpse",
	"brown pudding corpse",
	"green slime corpse",
	"black pudding corpse",
	"quantum mechanic corpse",
	"rust monster corpse",
	"disenchanter corpse",
	"garter snake corpse",
	"snake corpse",
	"water moccasin corpse",
	"python corpse",
	"pit viper corpse",
	"cobra corpse",
	"troll corpse",
	"ice troll corpse",
	"rock troll corpse",
	"water troll corpse",
	"Olog-hai corpse",
	"umber hulk corpse",
	"vampire corpse",
	"vampire lord corpse",
	"Vlad the Impaler corpse",
	"barrow wight corpse",
	"wraith corpse",
	"Nazgul corpse",
	"xorn corpse",
	"monkey corpse",
	"ape corpse",
	"owlbear corpse",
	"yeti corpse",
	"carnivorous ape corpse",
	"sasquatch corpse",
	"kobold zombie corpse",
	"gnome zombie corpse",
	"orc zombie corpse",
	"dwarf zombie corpse",
	"elf zombie corpse",
	"human zombie corpse",
	"ettin zombie corpse",
	"ghoul corpse",
	"giant zombie corpse",
	"skeleton corpse",
	"straw golem corpse",
	"paper golem corpse",
	"rope golem corpse",
	"gold golem corpse",
	"leather golem corpse",
	"wood golem corpse",
	"flesh golem corpse",
	"clay golem corpse",
	"stone golem corpse",
	"glass golem corpse",
	"iron golem corpse",
	"human corpse",
	"wererat corpse",
	"werejackal corpse",
	"werewolf corpse",
	"elf corpse",
	"Woodland-elf corpse",
	"Green-elf corpse",
	"Grey-elf corpse",
	"elf-lord corpse",
	"Elvenking corpse",
	"doppelganger corpse",
	"shopkeeper corpse",
	"guard corpse",
	"prisoner corpse",
	"Oracle corpse",
	"aligned priest corpse",
	"high priest corpse",
	"soldier corpse",
	"sergeant corpse",
	"nurse corpse",
	"lieutenant corpse",
	"captain corpse",
	"watchman corpse",
	"watch captain corpse",
	"Medusa corpse",
	"Wizard of Yendor corpse",
	"Croesus corpse",
	"ghost corpse",
	"shade corpse",
	"water demon corpse",
	"succubus corpse",
	"horned devil corpse",
	"incubus corpse",
	"erinys corpse",
	"barbed devil corpse",
	"marilith corpse",
	"vrock corpse",
	"hezrou corpse",
	"bone devil corpse",
	"ice devil corpse",
	"nalfeshnee corpse",
	"pit fiend corpse",
	"sandestin corpse",
	"balrog corpse",
	"Juiblex corpse",
	"Yeenoghu corpse",
	"Orcus corpse",
	"Geryon corpse",
	"Dispater corpse",
	"Baalzebub corpse",
	"Asmodeus corpse",
	"Demogorgon corpse",
	"Death corpse",
	"Pestilence corpse",
	"Famine corpse",
	"djinni corpse",
	"jellyfish corpse",
	"piranha corpse",
	"shark corpse",
	"giant eel corpse",
	"electric eel corpse",
	"kraken corpse",
	"newt corpse",
	"gecko corpse",
	"iguana corpse",
	"baby crocodile corpse",
	"lizard corpse",
	"chameleon corpse",
	"crocodile corpse",
	"salamander corpse",
	"long worm tail corpse",
	"archeologist corpse",
	"barbarian corpse",
	"caveman corpse",
	"cavewoman corpse",
	"healer corpse",
	"knight corpse",
	"monk corpse",
	"priest corpse",
	"priestess corpse",
	"ranger corpse",
	"rogue corpse",
	"samurai corpse",
	"tourist corpse",
	"valkyrie corpse",
	"wizard corpse",
	"Lord Carnarvon corpse",
	"Pelias corpse",
	"Shaman Karnov corpse",
	"Hippocrates corpse",
	"King Arthur corpse",
	"Grand Master corpse",
	"Arch Priest corpse",
	"Orion corpse",
	"Master of Thieves corpse",
	"Lord Sato corpse",
	"Twoflower corpse",
	"Norn corpse",
	"Neferet the Green corpse",
	"Minion of Huhetotl corpse",
	"Thoth Amon corpse",
	"Chromatic Dragon corpse",
	"Cyclops corpse",
	"Ixoth corpse",
	"Master Kaen corpse",
	"Nalzok corpse",
	"Scorpius corpse",
	"Master Assassin corpse",
	"Ashikaga Takauji corpse",
	"Lord Surtur corpse",
	"Dark One corpse",
	"student corpse",
	"chieftain corpse",
	"neanderthal corpse",
	"attendant corpse",
	"page corpse",
	"abbot corpse",
	"acolyte corpse",
	"hunter corpse",
	"thug corpse",
	"ninja corpse",
	"roshi corpse",
	"guide corpse",
	"warrior corpse",
	"apprentice corpse"
]

itemLookup = [
	2160,
	1906,
	1907,
	1908,
	1909,
	1910,
	1911,
	1912,
	1913,
	1914,
	1915,
	1916,
	1917,
	1918,
	1919,
	1920,
	1921,
	1922,
	1923,
	1924,
	1925,
	1926,
	1927,
	1928,
	1929,
	1930,
	1931,
	1932,
	1933,
	1934,
	1935,
	1936,
	1937,
	1938,
	1939,
	1940,
	1941,
	1942,
	1943,
	1944,
	1945,
	1946,
	1947,
	1948,
	1949,
	1950,
	1951,
	1952,
	1953,
	1954,
	1955,
	1956,
	1957,
	1958,
	1959,
	1960,
	1961,
	1962,
	1963,
	1964,
	1965,
	1966,
	1967,
	1968,
	1969,
	1970,
	1971,
	1972,
	1973,
	1974,
	1975,
	1976,
	1977,
	1978,
	1979,
	1980,
	1981,
	1982,
	1983,
	1984,
	1985,
	1986,
	1987,
	1988,
	1989,
	1990,
	1991,
	1992,
	1993,
	1994,
	1995,
	1996,
	1997,
	1998,
	1999,
	2000,
	2001,
	2002,
	2003,
	2004,
	2005,
	2006,
	2007,
	2008,
	2009,
	2010,
	2011,
	2012,
	2013,
	2014,
	2015,
	2016,
	2017,
	2018,
	2019,
	2020,
	2021,
	2022,
	2023,
	2024,
	2025,
	2026,
	2027,
	2028,
	2029,
	2030,
	2031,
	2032,
	2033,
	2034,
	2035,
	2036,
	2037,
	2038,
	2039,
	2040,
	2041,
	2042,
	2043,
	2044,
	2045,
	2046,
	2047,
	2048,
	2049,
	2050,
	2051,
	2052,
	2053,
	2054,
	2055,
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
	2083,
	2084,
	2085,
	2086,
	2087,
	2088,
	2089,
	2090,
	2091,
	2092,
	2093,
	2094,
	2095,
	2096,
	2097,
	2098,
	2099,
	2100,
	2101,
	2102,
	2103,
	2104,
	2105,
	2106,
	2107,
	2108,
	2109,
	2110,
	2111,
	2112,
	2113,
	2114,
	2115,
	2116,
	2117,
	2118,
	2177,
	2119,
	2120,
	2121,
	2122,
	2123,
	2124,
	2125,
	2126,
	2127,
	2128,
	2129,
	2130,
	2131,
	2132,
	2133,
	2134,
	2135,
	2136,
	2137,
	2138,
	2139,
	2140,
	2141,
	2142,
	2143,
	2144,
	2145,
	2146,
	2147,
	2148,
	2149,
	2150,
	2151,
	2152,
	2153,
	2154,
	2155,
	2156,
	2157,
	2158,
	2159,
	2161,
	2162,
	2163,
	2164,
	2165,
	2166,
	2167,
	2168,
	2169,
	2170,
	2171,
	2172,
	2173,
	2174,
	2175,
	2176,
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
	2202,
	2203,
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
	2244,
	2245,
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
	2285,
	2286,
	2287,
	2288,
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
	2315,
	2316,
	2317,
	2318,
	2319,
	2320,
	2321,
	2322,
	2323,
	2324,
	2325,
	2326,
	2327,
	2328,
	2329,
	2330,
	2331,
	2332,
	2333,
	2334,
	2335,
	2336,
	2337,
	2338,
	2339,
	2340,
	2341,
	2342,
	2343,
	2344,
	2345,
	2346,
	2347,
	2348,
	2349,
	2350,
	2351,
	2352,
	2353,
	2354,
	2355,
	2356,
	2357,
	2358,
	# Corpses start here
	1144,
	1145,
	1146,
	1147,
	1148,
	1149,
	1150,
	1151,
	1152,
	1153,
	1154,
	1155,
	1156,
	1157,
	1158,
	1159,
	1160,
	1161,
	1162,
	1163,
	1164,
	1165,
	1166,
	1167,
	1168,
	1169,
	1170,
	1171,
	1172,
	1173,
	1174,
	1175,
	1176,
	1177,
	1178,
	1179,
	1180,
	1181,
	1182,
	1183,
	1184,
	1185,
	1186,
	1187,
	1188,
	1189,
	1190,
	1191,
	1192,
	1193,
	1194,
	1195,
	1196,
	1197,
	1198,
	1199,
	1200,
	1201,
	1202,
	1203,
	1204,
	1205,
	1206,
	1207,
	1208,
	1209,
	1210,
	1211,
	1212,
	1213,
	1214,
	1215,
	1216,
	1217,
	1218,
	1219,
	1220,
	1221,
	1222,
	1223,
	1224,
	1225,
	1226,
	1227,
	1228,
	1229,
	1230,
	1231,
	1232,
	1233,
	1234,
	1235,
	1236,
	1237,
	1238,
	1239,
	1240,
	1241,
	1242,
	1243,
	1244,
	1245,
	1246,
	1247,
	1248,
	1249,
	1250,
	1251,
	1252,
	1253,
	1254,
	1255,
	1256,
	1257,
	1258,
	1259,
	1260,
	1261,
	1262,
	1263,
	1264,
	1265,
	1266,
	1267,
	1268,
	1269,
	1270,
	1271,
	1272,
	1273,
	1274,
	1275,
	1276,
	1277,
	1278,
	1279,
	1280,
	1281,
	1282,
	1283,
	1284,
	1285,
	1286,
	1287,
	1288,
	1289,
	1290,
	1291,
	1292,
	1293,
	1294,
	1295,
	1296,
	1297,
	1298,
	1299,
	1300,
	1301,
	1302,
	1303,
	1304,
	1305,
	1306,
	1307,
	1308,
	1309,
	1310,
	1311,
	1312,
	1313,
	1314,
	1315,
	1316,
	1317,
	1318,
	1319,
	1320,
	1321,
	1322,
	1323,
	1324,
	1325,
	1326,
	1327,
	1328,
	1329,
	1330,
	1331,
	1332,
	1333,
	1334,
	1335,
	1336,
	1337,
	1338,
	1339,
	1340,
	1341,
	1342,
	1343,
	1344,
	1345,
	1346,
	1347,
	1348,
	1349,
	1350,
	1351,
	1352,
	1353,
	1354,
	1355,
	1356,
	1357,
	1358,
	1359,
	1360,
	1361,
	1362,
	1363,
	1364,
	1365,
	1366,
	1367,
	1368,
	1369,
	1370,
	1371,
	1372,
	1373,
	1374,
	1375,
	1376,
	1377,
	1378,
	1379,
	1380,
	1381,
	1382,
	1383,
	1384,
	1385,
	1386,
	1387,
	1388,
	1389,
	1390,
	1391,
	1392,
	1393,
	1394,
	1395,
	1396,
	1397,
	1398,
	1399,
	1400,
	1401,
	1402,
	1403,
	1404,
	1405,
	1406,
	1407,
	1408,
	1409,
	1410,
	1411,
	1412,
	1413,
	1414,
	1415,
	1416,
	1417,
	1418,
	1419,
	1420,
	1421,
	1422,
	1423,
	1424,
	1425,
	1426,
	1427,
	1428,
	1429,
	1430,
	1431,
	1432,
	1433,
	1434,
	1435,
	1436,
	1437,
	1438,
	1439,
	1440,
	1441,
	1442,
	1443,
	1444,
	1445,
	1446,
	1447,
	1448,
	1449,
	1450,
	1451,
	1452,
	1453,
	1454,
	1455,
	1456,
	1457,
	1458,
	1459,
	1460,
	1461,
	1462,
	1463,
	1464,
	1465,
	1466,
	1467,
	1468,
	1469,
	1470,
	1471,
	1472,
	1473,
	1474,
	1475,
	1476,
	1477,
	1478,
	1479,
	1480,
	1481,
	1482,
	1483,
	1484,
	1485,
	1486,
	1487,
	1488,
	1489,
	1490,
	1491,
	1492,
	1493,
	1494,
	1495,
	1496,
	1497,
	1498,
	1499,
	1500,
	1501,
	1502,
	1503,
	1504,
	1505,
	1506,
	1507,
	1508,
	1509,
	1510,
	1511,
	1512,
	1513,
	1514,
	1515,
	1516,
	1517,
	1518,
	1519,
	1520,
	1521,
	1522,
	1523,
	1524
]