from mesa import Agent, Model
import random
import movement_control, rl_methods
import numpy as np
from collections import defaultdict
import copy


class MonteCarloAgent(Agent):
    """ Monte Carlo agent """
    
    def __init__(self, unique_id, model, Q_old, epsilon_ep):
        super().__init__(unique_id, model)
        print("creating monte carlo agent")
        nA = len(rl_methods.action_space)
        self.Q = Q_old # load previous episode Q table
        self.episilon = epsilon_ep # episilon calculated by episode
        self.states = []
        self.rewards = []
        self.actions = []
        
        # initialize empty dictionaries of arrays
        #Q = defaultdict(lambda: np.zeros(nA))
        #N = defaultdict(lambda: np.zeros(nA))
        #returns_sum = defaultdict(lambda: np.zeros(env.action_space.n))


    def step(self):
        print("monte carlo step")
        self.state = rl_methods.encode_state(self.model.grid)
        
        possible_steps = movement_control.find_empty_location(self.pos, self.model)
        if self.state in self.Q:
            action = self.mc_action_selection(possible_steps)
        else:
            action = random.choice(possible_steps)
            
        #save state, action
        self.actions.append(action)
        self.states.append(copy.deepcopy(self.state))
        
        self.move(action)

    def move(self,action):
        new_position = rl_methods.action_next_location(self, self.model.grid, action)
        #possible_steps = movement_control.find_empty_location(self.pos, self.model)
        #new_position = random.choice(possible_steps)
        #print(self.unique_id, " moving from ", self.pos, " to ", new_position)
        self.model.grid.move_agent(self, new_position)

    def mc_action_selection(self):
        return select_action(self.Q, self.epsilon, possible_steps, len(rl_methods.action_space), self.state)
        
    def get_variables(self):
        return Q
        
    def update_rewards(self):
        self.rewards.append(self.model.current_cow_count)
