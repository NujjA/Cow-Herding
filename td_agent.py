from mesa import Agent, Model
#import random
#import movement_control
#import numpy as np


class TDAgent(Agent):
    """ Temporal Difference agent """
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print("creating TD agent")
        # take previous w
        self.previousA = None
        self.previousS = None
        self.Aprime = None
        self.Sprime = None
        self.reward = None

    def step(self):
        print("TD step")
        # Choose an action A from S using Pi
        # take action A
        if(self.previousA):
            # there was a previousA, selectA prime and get Sprime
            # update w
            self.previousA = self.Aprime
            self.previousS = self.Sprime
            pass
        else:
            # there was not a previousA, select first previousA, store first previousS
            pass
            
        self.move()

    def move(self):
        # 
        possible_steps = movement_control.find_empty_location(self.pos, self.model)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def update_TDAgent(self, current_reward):
        ''' called by model at the end of the step '''
        # Observe R
        self.reward = current_reward
