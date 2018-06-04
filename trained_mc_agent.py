import rl_methods
from mesa import Agent, Model
import numpy as np
import random

class TrainedMonteCarloAgent(Agent):
    """ Pretrained Monte Carlo agent """
    
    def __init__(self, unique_id, model, Q_old, vision = None):
        super().__init__(unique_id, model)
        print("creating trained mc agent with vision range ", vision)
        nA = len(rl_methods.action_space)
        self.Q = Q_old # load previous episode Q table
        #self.epsilon = epsilon_ep # episilon calculated by episode
        #self.gamma = gamma
        #self.alpha = alpha
        #self.states = []
        #self.rewards = []
        #self.actions = []
        
        
        self.vision_range = vision


    def step(self):
        print("trained monte carlo step")
        if self.vision_range:
            self.state = rl_methods.encode_state_range(self, self.vision_range) 
            #print(self.state)
        else:
            self.state = rl_methods.encode_state(self.model.grid)
                
        possible_actions = rl_methods.possible_action_space(self)
        #print("Q: ", self.Q)
        Q_array = np.array(self.Q)
        print("Type Q: ", self.Q.dtype)
        #print("state: ", self.state)
        #print("Type state", type(self.state))
        if self.state in self.Q:
            #action = self.mc_action_selection(possible_actions)
            action = max_action = np.argmax(Q[state])
            print("The max action is ", action)
            if action not in possible_actions:
                action = random.choice(possible_actions)
                print("Max action not in possible actions, picking randomly")
        else:
            action = random.choice(possible_actions)
            print("I havent seen this before, picking randomly")
            
        
        self.move(action)

    def move(self,action):
        new_position = rl_methods.action_next_location(self, self.model.grid, action)
        self.model.grid.move_agent(self, new_position)

 #   def mc_action_selection(self, possible_steps):
 #       print("I've seen this before")
 #       return rl_methods.select_e_greedy_action(self.Q, self.epsilon, possible_steps, self.state)
        
#    def Q_table_update(self, shared_Q_table = None):
#        """Called by the model at the end of the episode to update the Q table"""        
#        if(shared_Q_table): # If sharing Q table, get the last updated Q table from the team
#            self.Q = shared_Q_table
#        for i in range(len(self.states)): #for each timestep
#            state = self.states[i]
#            action = self.actions[i]
#            reward = 0.0
#            for r in range(i, len(self.rewards)):
#                reward = reward + (self.rewards[r] * self.gamma**i)
#            prev_Q = self.Q[state][action]
#            self.Q[state][action] = prev_Q + (self.alpha * (reward - prev_Q))
#        return self.Q
        
 #   def update_rewards(self, reward):
 #       """Called by the model at the end of the step to get the reward for the current state and action"""
 #       self.rewards.append(float(reward))
