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
CONST_STATUS_UPDATE_PERIOD = 2000 # Print the map out every <#> steps
CONST_PRINT_MAP_DURING_FLOOR_TRANSITION = False # I mean... this prints the map during floor transition. What else can I say?

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
		