#!/usr/bin/python

# This file adds more printing to console.
# Note: This isn't intended to have ALL the printing this agent will ever do.
# Feel free to add printing elsewhere.
# That being said, let's keep all constants related to printing here,
# so they're all in one place, nice and organized.

from .items import *
from .gamestate import *
from .utilities import *

CONST_QUIET = False # Enable to silence all prints about gamestate except fatal errors
CONST_STATUS_UPDATE_PERIOD = 1999 # Print the map out every <#> steps
	# Changed from 2000 to 1999. 1999 is better because it's prime.
	# Why is that important? Well, sometimes the agent gets stuck in a loop where it sees the same sequence of 2-4 messages on loop forever.
	# If update period is a multiple of the sequence length we only ever see one message in that loop no matter how many status reports we do.
	# Making update period prime means that a repeating sequence of N messages will be fully reported within N status reports.
	# Modular arithmetic for the win!
CONST_PRINT_MAP_DURING_FLOOR_TRANSITION = False # I mean... this prints the map during floor transition. What else can I say?
CONST_REPORT_KILLS = False # If true, prints a message whenever the agent directly kills a monster

statusAfflictionLabels = [
	"[STONING]", # stoning
	"[SLIMING]", # sliming
	"[STRANGLED]", # strangulation
	"[FOOD POISONING]", # food poisoning
	"[DISEASE]", # disease
	"[blindness]", # blindness
	"[deafness]", # deafness
	"[stunned]", # stunning
	"[confused]", # confusion
	"[hallucinating]", # hallucination
	"[levitating]", # levitation
	"[flying]", # flight
	"[riding]" # riding
]

statusAfflictionMessages = [
	"CRITICAL: Agent is petrifying!!", # stoning
	"URGENT: Agent is sliming!!", # sliming
	"URGENT: Amulet of Strangulation!", # strangulation
	"WARNING: Agent ate something tainted!", # food poisoning
	"WARNING: Agent is withering away!", # disease
	"Agent can't see!", # blindness
	"Agent can't hear!", # deafness
	"Agent staggers!", # stunning
	"Agent is lightheaded!", # confusion
	"Agent's observations are compromised!", # hallucination
	"Agent is floating in mid-air.", # levitation
	"Agent takes to the air.", # flight
	"Agent mounts their faithful steed." # riding
]

statusCuredMessages = [
	"Phew... Agent is no longer petrifying.", # stoning
	"Phew... the slime is purged.", # sliming
	"Phew... the agent can breathe.", # strangulation
	"Phew... agent's stomach settles.", # food poisoning
	"Phew... agent is cured.", # disease
	"Agent can see again.", # blindness
	"Agent can hear again.", # deafness
	"Agent regains balance.", # stunning
	"Agent's eyes regain focus.", # confusion
	"Agent's observations are restored.", # hallucination
	"Agent's feet return to the ground.", # levitation
	"Agent lands.", # flight
	"Agent dismounts." # riding
]

def narrateGame(state, observations):
	if CONST_QUIET:
		return
	state.narrationStatus["report_timer"] -= 1
	if state.narrationStatus["report_timer"] <= 0:
		state.statusReport(observations)
	
	hpRatio = observations["blstats"][10] / observations["blstats"][11]
	if hpRatio == 1 and state.narrationStatus["hp_threshold"] > 0:
		state.narrationStatus["hp_threshold"] = 0 # Full health, reset the alarm to trip again later
		print("Phew... HP back to full.")
	if hpRatio <= 0.25 and state.narrationStatus["hp_threshold"] <= 1:
		state.narrationStatus["hp_threshold"] = 2 # Alarm tripped, don't trip again until HP is restored
		print("Agent's HP is critically low!")
		print("Situation: \"" + readMessage(observations) + "\"")
	if hpRatio <= 0.5 and state.narrationStatus["hp_threshold"] == 0:
		state.narrationStatus["hp_threshold"] = 1 # Alarm semi-tripped, alarm can still be tripped if HP drops further
		print("Agent's HP has dropped to half.")
	
	if state.narrationStatus["hunger_threshold"] == 0 and observations["blstats"][21] >= 3:
		state.narrationStatus["hunger_threshold"] = 1 # Alarm tripped, don't trip again until nutrition is restored
		print("Agent is dangerously hungry!")
	if state.narrationStatus["hunger_threshold"] == 1 and observations["blstats"][21] <= 1:
		state.narrationStatus["hunger_threshold"] = 0 # Reset the alarm to trip again later
		print("Phew... Agent is a bit less hungry now.")
	
	if state.narrationStatus["weight_threshold"] == 0 and observations["blstats"][22] >= 1:
		state.narrationStatus["weight_threshold"] = 1 # Alarm tripped, don't trip again until encumbrance is lowered
		print("Agent is weighed down!")
	if state.narrationStatus["weight_threshold"] == 1 and observations["blstats"][22] == 0:
		state.narrationStatus["weight_threshold"] = 0 # Reset the alarm to trip again later
		print("Agent is no longer weighed down.")
	
	if readMessage(observations).find("You feel feverish") != -1:
		print("Agent is infected with lycanthropy!")
	
	for x in range(13):
		if readHeroStatus(observations, x) and not state.narrationStatus["status"][x]:
			state.narrationStatus["status"][x] = True
			#print(statusAfflictionMessages[x])
			print("\"" + readMessage(observations) + "\" " + statusAfflictionLabels[x])
			if x == 3:
				#print("Culprit: ", state.corpseMap[readDungeonLevel(observations)][readHeroRow(observations)][readHeroCol(observations)])
				print("Current turn: ", readTurn(observations))
		if (not readHeroStatus(observations, x)) and state.narrationStatus["status"][x]:
			state.narrationStatus["status"][x] = False
			print(statusCuredMessages[x])
	
	"""
	if readMessage(observations).find("You don't have that object") != -1 and not state.criticalSituation:
		print("Spotted the don't-have-that issue. Inventory:")
		for x in range(len(observations["inv_strs"])):
			print("\t" + chr(observations["inv_letters"][x]) + ": ",end="")
			print("\""+readInventoryItemDesc(observations, x)+'"')
		state.criticalSituation = True
	"""
	
	if state.criticalSituation:
		print("\"",readMessage(observations),"\"")