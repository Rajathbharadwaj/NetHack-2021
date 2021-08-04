#!/usr/bin/python

# Here we have a nice little reference of corpses and how willing we are to eat them
# The number given is the lowest hunger level where we'll consider eating it
# Just as reference:
	# 0 = satiated
	# 1 = ok
	# 2 = hungry
	# 3 = weak
	# 4 = fainting

corpsePriority = {
	1144 : 2, # giant ant
	1145 : 4, # killer bee (poisonous, can drain strength) (30% for poison resistance)
	1146 : 4, # soldier ant (poisonous) (20% for poison resistance)
	1147 : 0, # fire ant (20% for fire resistance)
	1148 : 4, # giant beetle (poisonous) (33% for poison resistance)
	1149 : 3, # queen bee (poisonous) (60% for poison resistance)
	1150 : 4, # acid blob (acidic) (cures petrification)
	1151 : 2, # quivering blob (33% for poison resistance)
	1152 : 3, # gelatinous cube (acidic) (10% each for fire, cold, shock, and sleep resistance)
	1153 : 5, # chickatrice (turns you to stone) (27% for poison resistance)
	1154 : 5, # cockatrice (turns you to stone) (33% for poison resistance)
	1155 : 1, # pyrolisk (20% each for fire and poison resistance)
	1156 : 1, # jackal (can count as cannibalism if you've been infected by a werejackal)
	1157 : 1, # fox
	1158 : 1, # coyote
	1159 : 4, # werejackal (lycanthropic, counts as cannibalism for humans)
	1160 : 4, # little dog (aggravate monster)
	1161 : 1, # dingo
	1162 : 4, # dog (aggravate monster)
	1163 : 4, # large dog (aggravate monster)
	1164 : 1, # wolf (can count as cannibalism if you've been infected by a werewolf)
	1165 : 4, # werewolf (lycanthropic, counts as cannibalism for humans)
	1166 : 1, # winter wolf cub (33% for cold resistance)
	1167 : 1, # warg
	1168 : 1, # winter wolf (47% for cold resistance)
	1169 : 1, # hell hound pup (47% for fire resistance)
	1170 : 1, # hell hound (80% for fire resistance)
	1171 : 1, # gas spore (never leaves a corpse)
	1172 : 0, # floating eye (100% for telepathy)
	1173 : 1, # freezing sphere (never leaves a corpse)
	1174 : 1, # flaming sphere (never leaves a corpse)
	1175 : 1, # shocking sphere (never leaves a corpse)
	1176 : 4, # kitten (aggravate monster)
	1177 : 4, # housecat (aggravate monster)
	1178 : 1, # jaguar
	1179 : 1, # lynx
	1180 : 1, # panther
	1181 : 4, # large cat (aggravate monster)
	1182 : 1, # tiger
	1183 : 4, # gremlin (poisonous) (33% for poison resistance)
	1184 : 1, # gargoyle
	1185 : 1, # winged gargoyle
	1186 : 1, # hobbit
	1187 : 4, # dwarf (counts as cannibalism for dwarves)
	1188 : 1, # bugbear
	1189 : 4, # dwarf lord (counts as cannibalism for dwarves)
	1190 : 4, # dwarf king (counts as cannibalism for dwarves)
	1191 : 1, # mind flayer (50% each for telepathy and intelligence)
	1192 : 1, # master mind flayer (50% each for telepathy and intelligence)
	1193 : 1, # manes (never leaves a corpse)
	1194 : 4, # homunculus (poisonous) (7% each for sleep and poison resistance)
	1195 : 1, # imp
	1196 : 3, # lemure (poisonous) (sleep resistance)
	1197 : 1, # quasit (20% for poison resistance)
	1198 : 4, # tengu (13% for poison resistance, 17% for teleport control, 20% for teleporitis)
	1199 : 1, # blue jelly (13% each for poison and cold resistance)
	1200 : 4, # spotted jelly (acidic)
	1201 : 4, # ochre jelly (acidic)
	1202 : 4, # kobold (poisonous)
	1203 : 4, # large kobold (poisonous)
	1204 : 4, # kobold lord (poisonous)
	1205 : 4, # kobold shaman (poisonous)
	1206 : 4, # leprechaun (50% for teleportitis)
	1207 : 1, # small mimic (makes you mimic gold for a bit)
	1208 : 1, # large mimic (makes you mimic gold for a bit)
	1209 : 1, # giant mimic (makes you mimic gold for a bit)
	1210 : 4, # wood nymph (30% for teleportitis)
	1211 : 4, # water nymph (30% for teleportitis)
	1212 : 4, # mountain nymph (30% for teleportitis)
	1213 : 1, # goblin
	1214 : 1, # hobgoblin
	1215 : 1, # orc
	1216 : 1, # hill orc
	1217 : 1, # mordor orc
	1218 : 1, # uruk-hai
	1219 : 1, # orc shaman
	1220 : 1, # orc-captain
	1221 : 1, # rock piercer
	1222 : 1, # iron piercer
	1223 : 1, # glass piercer
	1224 : 1, # rothe
	1225 : 1, # mumak
	1226 : 1, # leocrotta
	1227 : 1, # wumpus
	1228 : 1, # titanothere
	1229 : 2, # baluchitherium (800 nutrition)
	1230 : 2, # mastodon (800 nutrition)
	1231 : 1, # sewer rat
	1232 : 1, # giant rat
	1233 : 4, # rabid rat (poisonous)
	1234 : 4, # wererat (lycanthropic, counts as cannibalism for humans)
	1235 : 1, # rock mole
	1236 : 1, # woodchuck
	1237 : 1, # cave spider (7% for poison resistance)
	1238 : 1, # centipede (13% for poison resistance)
	1239 : 4, # giant spider (poisonous) (33% for poison resistance)
	1240 : 4, # scorpion (poisonous) (50% for poison resistance)
	1241 : 1, # lurker above
	1242 : 1, # trapper
	1243 : 1, # pony
	1244 : 1, # black unicorn (27% for poison resistance)
	1245 : 1, # gray unicorn (27% for poison resistance)
	1246 : 1, # white unicorn (27% for poison resistance)
	1247 : 1, # horse
	1248 : 1, # warhorse
	1249 : 1, # fog cloud (never leaves a corpse)
	1250 : 1, # dust vortex (never leaves a corpse)
	1251 : 1, # ice vortex (never leaves a corpse)
	1252 : 1, # energy vortex (never leaves a corpse)
	1253 : 1, # steam vortex (never leaves a corpse)
	1254 : 1, # fire vortex (never leaves a corpse)
	1255 : 1, # baby long worm
	1256 : 1, # baby purple worm
	1257 : 1, # long worm
	1258 : 2, # purple worm (700 nutrition)
	1259 : 1, # grid bug (never leaves a corpse)
	1260 : 4, # xan (poisonous) (47% for poison resistance)
	1261 : 1, # yellow light (never leaves a corpse)
	1262 : 1, # black light (never leaves a corpse)
	1263 : 1, # zruty
	1264 : 4, # couatl (never leaves a corpse)
	1265 : 1, # aleax (never leaves a corpse)
	1266 : 1, # angel (never leaves a corpse)
	1267 : 1, # ki-rin (never leaves a corpse)
	1268 : 1, # Archon (never leaves a corpse)
	1269 : 3, # bat (stuns when eaten)
	1270 : 4, # giant bat (stuns long when eaten)
	1271 : 1, # raven
	1272 : 4, # vampire bat (poisonous)
	1273 : 1, # plains centaur
	1274 : 1, # forest centaur
	1275 : 1, # mountain centaur
	1276 : 1, # baby gray dragon
	1277 : 1, # baby silver dragon
	1278 : 1, # baby red dragon
	1279 : 1, # baby white dragon
	1280 : 1, # baby orange dragon
	1281 : 1, # baby black dragon
	1282 : 1, # baby blue dragon
	1283 : 4, # baby green dragon (poisonous)
	1284 : 4, # baby yellow dragon (acidic) (cures petrification)
	1285 : 3, # gray dragon (1500 nutrition)
	1286 : 3, # silver dragon (1500 nutrition)
	1287 : 2, # red dragon (1500 nutrition) (fire resistance)
	1288 : 2, # white dragon (1500 nutrition) (cold resistance) 
	1289 : 2, # orange dragon (1500 nutrition) (sleep resistance)
	1290 : 1, # black dragon (1500 nutrition) (disintegration resistance)
	1291 : 2, # blue dragon (1500 nutrition) (shock resistance)
	1292 : 4, # green dragon (1500 nutrition, poisonous) (poison resistance)
	1293 : 4, # yellow dragon (1500 nutrition, acidic) (cures petrification)
	1294 : 3, # stalker (stuns when eaten) (temporary invisibility, or permanent + see invisible if already invisible)
	1295 : 1, # air elemental (never leaves a corpse)
	1296 : 1, # fire elemental (never leaves a corpse)
	1297 : 1, # earth elemental (never leaves a corpse)
	1298 : 1, # water elemental (never leaves a corpse)
	1299 : 1, # lichen (NON-PERISHABLE)
	1300 : 1, # brown mold (3% each for cold and poison resistance)
	1301 : 4, # yellow mold (poisonous, hallucinogenic) 
	1302 : 4, # green mold (acidic)
	1303 : 1, # red mold (3% each for fire and poison resistance)
	1304 : 1, # shrieker (20% for poison resistance)
	1305 : 4, # violet fungus (hallucinogenic) (20% for poison resistance)
	1306 : 4, # gnome (counts as cannibalism for gnomes)
	1307 : 4, # gnome lord (counts as cannibalism for gnomes)
	1308 : 4, # gnomish wizard (counts as cannibalism for gnomes)
	1309 : 4, # gnome king (counts as cannibalism for gnomes)
	1310 : 4, # giant (uhhh... is this actually a thing? looks like giants only come in specific kinds, not generic)
	1311 : 2, # stone giant (750 nutrition) (50% for strength)
	1312 : 2, # hill giant (700 nutrition) (50% for strength)
	1313 : 2, # fire giant (750 nutrition) (30% for fire resistance, 50% for strength)
	1314 : 2, # frost giant (750 nutrition) (33% for cold resistance, 50% for strength)
	1315 : 1, # ettin
	1316 : 2, # storm giant (750 nutrition) (50% each for shock resistance and strength)
	1317 : 2, # titan (900 nutrition)
	1318 : 2, # minotaur (700 nutrition)
	1319 : 1, # jabberwock
	1320 : 4, # Keystone Kop (counts as cannibalism for humans)
	1321 : 4, # Kop Sergeant (counts as cannibalism for humans)
	1322 : 4, # Kop Lieutenant (counts as cannibalism for humans)
	1323 : 4, # Kop Kaptain (counts as cannibalism for humans)
	1324 : 1, # lich (never leaves a corpse)
	1325 : 1, # demilich (never leaves a corpse)
	1326 : 1, # master lich (never leaves a corpse)
	1327 : 1, # arch-lich (never leaves a corpse)
	1328 : 1, # kobold mummy (doesn't have unique corpse)
	1329 : 1, # gnome mummy (doesn't have unique corpse)
	1330 : 1, # orc mummy (doesn't have unique corpse)
	1331 : 1, # dwarf mummy (doesn't have unique corpse)
	1332 : 1, # elf mummy (doesn't have unique corpse)
	1333 : 1, # human mummy (doesn't have unique corpse)
	1334 : 1, # ettin mummy (doesn't have unique corpse)
	1335 : 1, # giant mummy (doesn't have unique corpse)
	1336 : 1, # red naga hatchling (10% each for fire and poison resistance)
	1337 : 4, # black naga hatchling (acidic) (20% for poison resistance)
	1338 : 1, # golden naga hatchling (20% for poison resistance)
	1339 : 1, # guardian naga hatchling (20% for poison resistance)
	1340 : 1, # red naga (20% each for fire and poison resistance)
	1341 : 4, # black naga (acidic) (53% for poison resistance)
	1342 : 1, # golden naga (67% for poison resistance)
	1343 : 1, # guardian naga (80% for poison resistance)
	1344 : 1, # ogre
	1345 : 2, # ogre lord (700 nutrition)
	1346 : 2, # ogre king (750 nutrition)
	1347 : 1, # gray ooze (leaves a glob, not a corpse)
	1348 : 1, # brown pudding (leaves a glob, not a corpse)
	1349 : 1, # green slime (leaves a glob, not a corpse)
	1350 : 1, # black pudding (leaves a glob, not a corpse)
	1351 : 4, # quantum mechanic (poisonous) (toggles speed)
	1352 : 1, # rust monster
	1353 : 4, # disenchanter (deletes a random intrinsic)
	1354 : 1, # garter snake
	1355 : 4, # snake (poisonous) (27% for poison resistance)
	1356 : 4, # water moccasin (poisonous) (27% for poison resistance)
	1357 : 1, # python
	1358 : 4, # pit viper (poisonous) (40% for poison resistance)
	1359 : 4, # cobra (poisonous) (40% for poison resistance)
	1360 : 1, # troll (corpse can revive)
	1361 : 1, # ice troll (60% for cold resistance, corpse can revive)
	1362 : 1, # rock troll (corpse can revive)
	1363 : 1, # water troll (corpse can revive)
	1364 : 1, # Olog-hai (corpse can revive)
	1365 : 1, # umber hulk
	1366 : 4, # vampire (poisonous)
	1367 : 4, # vampire lord (poisonous)
	1368 : 1, # Vlad the Impaler (never leaves a corpse)
	1369 : 1, # barrow wight (never leaves a corpse)
	1370 : 0, # wraith (nutrition: 0, LEVEL UP!!)
	1371 : 1, # Nazgul (never leaves a corpse)
	1372 : 2, # xorn (nutrition: 700)
	1373 : 1, # monkey
	1374 : 1, # ape
	1375 : 2, # owlbear (nutrition: 700)
	1376 : 2, # yeti (nutrition: 700) (33% for cold resistance)
	1377 : 1, # carnivorous ape
	1378 : 2, # sasquatch (nutrition: 750)
	1379 : 1, # kobold zombie (doesn't have unique corpse)
	1380 : 1, # gnome zombie (doesn't have unique corpse)
	1381 : 1, # orc zombie (doesn't have unique corpse)
	1382 : 1, # dwarf zombie (doesn't have unique corpse)
	1383 : 1, # elf zombie (doesn't have unique corpse)
	1384 : 1, # human zombie (doesn't have unique corpse)
	1385 : 1, # ettin zombie (doesn't have unique corpse)
	1386 : 1, # ghoul (never leaves a corpse)
	1387 : 1, # giant zombie (doesn't have unique corpse)
	1388 : 1, # skeleton (never leaves a corpse)
	1389 : 1, # straw golem (never leaves a corpse)
	1390 : 1, # paper golem (never leaves a corpse)
	1391 : 1, # rope golem (never leaves a corpse)
	1392 : 1, # gold golem (never leaves a corpse)
	1393 : 1, # leather golem (never leaves a corpse)
	1394 : 1, # wood golem (never leaves a corpse)
	1395 : 1, # flesh golem (12% each for fire, cold, sleep, shock, and poison resistance)
	1396 : 1, # clay golem (never leaves a corpse)
	1397 : 1, # stone golem (never leaves a corpse)
	1398 : 1, # glass golem (never leaves a corpse)
	1399 : 1, # iron golem (never leaves a corpse)
	1400 : 4, # human (counts as cannibalism for humans)
	1401 : 4, # wererat (counts as cannibalism for humans)
	1402 : 4, # werejackal (counts as cannibalism for humans)
	1403 : 4, # werewolf (counts as cannibalism for humans)
	1404 : 4, # elf (counts as cannibalism for elves) (67% for sleep resistance)
	1405 : 4, # Woodland-elf (counts as cannibalism for elves) (27% for sleep resistance)
	1406 : 4, # Green-elf (counts as cannibalism for elves) (33% for sleep resistance)
	1407 : 4, # Grey-elf (counts as cannibalism for elves) (40% for sleep resistance)
	1408 : 4, # elf-lord (counts as cannibalism for elves) (53% for sleep resistance)
	1409 : 4, # Elvenking (counts as cannibalism for elves) (60% for sleep resistance)
	1410 : 4, # doppelganger (polymorphs when eaten, counts as cannibalism for humans)
	1411 : 4, # shopkeeper (counts as cannibalism for humans)
	1412 : 4, # guard (counts as cannibalism for humans)
	1413 : 4, # prisoner (counts as cannibalism for humans)
	1414 : 4, # Oracle (counts as cannibalism for humans)
	1415 : 4, # aligned priest (counts as cannibalism for humans)
	1416 : 4, # high priest (counts as cannibalism for humans)
	1417 : 4, # soldier (counts as cannibalism for humans)
	1418 : 4, # sergeant (counts as cannibalism for humans)
	1419 : 4, # nurse (counts as cannibalism for humans)
	1420 : 4, # lieutenant (counts as cannibalism for humans)
	1421 : 4, # captain (counts as cannibalism for humans)
	1422 : 4, # watchman (counts as cannibalism for humans)
	1423 : 4, # watch captain (counts as cannibalism for humans)
	1424 : 5, # medusa (turns you to stone) (100% for poison resistance)
	1425 : 4, # Wizard of Yendor (counts as cannibalism for humans)
	1426 : 4, # Croesus (counts as cannibalism for humans)
	1427 : 1, # ghost (never leaves a corpse)
	1428 : 1, # shade (never leaves a corpse)
	1429 : 1, # water demon (never leaves a corpse)
	1430 : 1, # succubus (never leaves a corpse)
	1431 : 1, # horned devil (never leaves a corpse)
	1432 : 1, # incubus (never leaves a corpse)
	1433 : 1, # erinys (never leaves a corpse)
	1434 : 1, # barbed devil (never leaves a corpse)
	1435 : 1, # marilith (never leaves a corpse)
	1436 : 1, # vrock (never leaves a corpse)
	1437 : 1, # hezrou (never leaves a corpse)
	1438 : 1, # bone devil (never leaves a corpse)
	1439 : 1, # ice devil (never leaves a corpse)
	1440 : 1, # nalfeshnee (never leaves a corpse)
	1441 : 1, # pit fiend (never leaves a corpse)
	1442 : 1, # sandestin (never leaves a corpse)
	1443 : 1, # balrog (never leaves a corpse)
	1444 : 1, # Juiblex (never leaves a corpse)
	1445 : 1, # Yeenoghu (never leaves a corpse)
	1446 : 1, # Orcus (never leaves a corpse)
	1447 : 1, # Geryon (never leaves a corpse)
	1448 : 1, # Dispater (never leaves a corpse)
	1449 : 1, # Baalzebub (never leaves a corpse)
	1450 : 1, # Asmodeus (never leaves a corpse)
	1451 : 1, # Demogorgon (wait, you actually killed him?! O_O)
	1452 : 999, # Death (DO. NOT. EAT.)
	1453 : 999, # Pestilence (DO. NOT. EAT.)
	1454 : 999, # Famine (DO. NOT. EAT.)
	1455 : 1, # djinni (never leaves a corpse)
	1456 : 4, # jellyfish (poisonous) (poison resistance)
	1457 : 1, # piranha
	1458 : 1, # shark
	1459 : 1, # giant eel
	1460 : 1, # electric eel (47% for shock resistance)
	1461 : 2, # kraken (nutrition: 1000)
	1462 : 0, # newt (at full Pw, 11% for +1 max Pw)
	1463 : 1, # gecko
	1464 : 1, # iguana
	1465 : 1, # baby crocodile
	1466 : 1, # lizard (NON-PERISHABLE, cures petrification)
	1467 : 4, # polymorphs when eaten
	1468 : 2, # crocodile
	1469 : 4, # salamander (poisonous) (53% for fire resistance)
	1470 : 1, # long worm tail (never leaves a corpse)
	1471 : 4, # archaeologist (counts as cannibalism for humans)
	1472 : 4, # barbarian (counts as cannibalism for hummans)
	1473 : 4, # caveman (counts as cannibalism for humans)
	1474 : 4, # cavewoman (counts as cannibalism for humans)
	1475 : 4, # healer (counts as cannibalism for humans)
	1476 : 4, # knight (counts as cannibalism for humans)
	1477 : 4, # monk (counts as cannibalism for humans)
	1478 : 4, # priest (counts as cannibalism for humans)
	1479 : 4, # priestess (counts as cannibalism for humans)
	1480 : 4, # ranger (counts as cannibalism for humans)
	1481 : 4, # rogue (counts as cannibalism for humans)
	1482 : 4, # samurai (counts as cannibalism for humans)
	1483 : 4, # tourist (counts as cannibalism for humans)
	1484 : 4, # valkyrie (counts as cannibalism for humans)
	1485 : 4, # wizard (counts as cannibalism for humans)
	1486 : 4, # Lord Carnarvon (counts as cannibalism for humans, also don't kill quest leader)
	1487 : 4, # Pelias (counts as cannibalism for humans, also don't kill quest leader)
	1488 : 4, # Shaman Karnov (counts as cannibalism for humans, also don't kill quest leader)
	1489 : 4, # Hippocrates (counts as cannibalism for humans, also don't kill quest leader)
	1490 : 4, # King Arthur (counts as cannibalism for humans, also don't kill quest leader)
	1491 : 4, # Grand Master (counts as cannibalism for humans, also don't kill quest leader)
	1492 : 4, # Arch Priest (counts as cannibalism for humans, also don't kill quest leader)
	1493 : 4, # Orion (counts as cannibalism for humans, also don't kill quest leader)
	1494 : 4, # Master of Thieves (counts as cannibalism for humans, also don't kill quest leader, unless he's actually quest nemesis)
	1495 : 4, # Lord Sato (counts as cannibalism for humans, also don't kill quest leader)
	1496 : 4, # Twoflower (counts as cannibalism for humans, also don't kill quest leader)
	1497 : 4, # Norn (counts as cannibalism for humans, also don't kill quest leader)
	1498 : 4, # Neferet the Green (counts as cannibalism for humans, also don't kill quest leader)
	1499 : 1, # Minion of Tutehotl (never leaves a corpse)
	1500 : 4, # Thoth Amon (counts as cannibalism for humans)
	1501 : 1, # Chromatic Dragon (Nutrition: 1700) (17% each for fire, cold, sleep, shock, disintegration, and poison resistance)
	1502 : 2, # Cyclops (Nutrition: 700) (50% for strength)
	1503 : 2, # Ixoth (1500 nutrition) (fire resistance)
	1504 : 4, # Master Kaen (counts as cannibalism for humans)
	1505 : 1, # Nalzok (never leaves a corpse)
	1506 : 1, # Scorpius (poison resistance)
	1507 : 4, # Master Assassin (counts as cannibalism for humans)
	1508 : 1, # Ashikaga Takauji (never leaves a corpse)
	1509 : 2, # Lord Surtur (Nutrition: 750) (50% each for fire resistance and strength)
	1510 : 4, # Dark One (counts as cannibalism for humans)
	1511 : 4, # student (counts as cannibalism for humans)
	1512 : 4, # chieftain (counts as cannibalism for humans)
	1513 : 4, # neanderthal (counts as cannibalism for humans)
	1514 : 4, # attendant (counts as cannibalism for humans)
	1515 : 4, # page (counts as cannibalism for humans)
	1516 : 4, # abbot (counts as cannibalism for humans)
	1517 : 4, # acolyte (counts as cannibalism for humans)
	1518 : 4, # hunter (counts as cannibalism for humans)
	1519 : 4, # thug (counts as cannibalism for humans)
	1520 : 4, # ninja (counts as cannibalism for humans)
	1521 : 4, # roshi (counts as cannibalism for humans)
	1522 : 4, # guide (counts as cannibalism for humans)
	1523 : 4, # warrior (counts as cannibalism for humans)
	1524 : 4, # apprentice (counts as cannibalism for humans)
}