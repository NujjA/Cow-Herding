from mesa import Agent, Model
from mesa.time import RandomActivation
import random

class RandomAgent(Agent):
    """ An agent that moves around randomly."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass
        #self.move()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
