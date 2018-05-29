from mesa import Agent, Model
#import random
#import movement_control
#import numpy as np


class MonteCarloAgent(Agent):
    """ Monte Carlo agent """
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print("creating monte carlo agent")

    def step(self):
        print("monte carlo step")
        self.move()

    def move(self):
        possible_steps = movement_control.find_empty_location(self.pos, self.model)
        new_position = random.choice(possible_steps)
        #print(self.unique_id, " moving from ", self.pos, " to ", new_position)
        self.model.grid.move_agent(self, new_position)
