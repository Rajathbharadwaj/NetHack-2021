#!/usr/bin/env python3

# TODO

# The value of a weapon is determined by the following:
	# The to-hit bonus of the weapon (higher = more value)
	# The damage output of the weapon (higher = more value)
	# The agent's current skill level with that weapon type (higher = more value)
	# The agent's maximum skill level with that weapon type (higher = more value)
	# The viability of that weapon's skill (more viability = more value)
		# example: sling proficiency is worthless late game, so high max sling skill isn't worth much
	# Whether the weapon is silver (yes = more value... unless the agent has been afflicted with silver-hating)
	# Whether the weapon is cursed (yes = less value)
		# (a weapon being cursed should apply a flat penalty to total value.)
		# (if an weapon is super strong on its own merit, we might wield it despite the curse.)
	# Whether we already have a better weapon for that slot (yes = less value)
	# Whether the agent is a monk (yes = less value)