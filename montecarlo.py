from mesa import Agent, Model
import random
import movement_control, rl_methods
import numpy as np
from collections import defaultdict


class MonteCarloAgent(Agent):
    """ Monte Carlo agent """
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print("creating monte carlo agent")
        nA = len(rl_methods.action_space)
        # initialize empty dictionaries of arrays
        Q = defaultdict(lambda: np.zeros(nA))
        N = defaultdict(lambda: np.zeros(nA))
        returns_sum = defaultdict(lambda: np.zeros(env.action_space.n))


    def step(self):
        print("monte carlo step")
        action = self.mc_action_selection()
        self.move()

    def move(self):
        possible_steps = movement_control.find_empty_location(self.pos, self.model)
        new_position = random.choice(possible_steps)
        #print(self.unique_id, " moving from ", self.pos, " to ", new_position)
        self.model.grid.move_agent(self, new_position)

    def mc_action_selection(self):
        return 0
        
    def get_variables(self):
        return Q