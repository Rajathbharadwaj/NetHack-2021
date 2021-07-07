import numpy as np

from agents.base import BatchedAgent
from agents.organized_agent_backend.gamestate import Gamestate
from agents.organized_agent_backend.behaviors import chooseAction


class OrganizedAgent(BatchedAgent):

    def __init__(self, num_envs, num_actions):
        # Setup goes here
        super().__init__(num_envs, num_actions)
        self.seeded_state = np.random.RandomState(42)
        self.state = []
        for x in range(num_envs):
            self.state.append(Gamestate())

    def batched_step(self, observations, rewards, dones, infos):
        """
        Perform a batched step on lists of environment outputs.

        Each argument is a list of the respective gym output.
        Returns an iterable of actions.
        """
        
        # Agent Name: Organized Dungeoneer – Has a list of priorities he checks in order, but is less of a spaghetti-coded mess
        
        actions = []
        for x in range(self.num_envs):
            if dones[x]:
                self.state[x].reset()
            actions.append(chooseAction(self.state[x], observations[x]))
        return actions
