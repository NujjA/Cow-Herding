from mesa.space import SingleGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from wall import WallAgent
from random_agent import RandomAgent
from plan_agent import PlanAgent
from cow_agent import CowAgent
from montecarlo import MonteCarloAgent
from td_agent import TDAgent
import cow_methods
import numpy as np
import rl_methods
#from mesa.datacollection import DataCollector
from movement_control import compute_score
import copy
from collections import defaultdict


class CHModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, height, random_n = 0, cow_n = 0, plan_n = 0, mc_n = 0, td_n = 0, episode_number = 0, old_Q_values = None):
        self.running = True 
        #self.num_agents = N
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        
        self.id_count = 0 #to assign each agent a unique ID
        self.max_timesteps = 500 #max timesteps for each episode
        
        # To keep score
        self.total_cow_count = 0.0
        self.current_cow_count = 0.0
        self.score = 0.0
        
        # Save model for agent use
        self.wallLocations = [(1,5), (1,6), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (6,6), (6,5)]
        self.goalState = [(2,5), (3,5), (4,5), (5,5), (2,6), (3,6), (4,6), (5,6)]
        self.goalTarget = (3,5) #corral "entrance" that plan agents herd towards
        self.state = None # encode state at each timestep
        
        self.number_random_agents = random_n
        self.number_cow_agents = cow_n
        self.number_plan_agents = plan_n
        self.number_monte_carlo_agents = mc_n
        self.number_td_agents = td_n
        
        # Monte Carlo Agent model save
        if old_Q_values:
            self.Q_values = old_Q_values
        else:
            self.Q_values = []
            for agent in range(self.number_monte_carlo_agents):
                self.Q_values.append(defaultdict(lambda: np.zeros(len(rl_methods.action_space))))
        self.mc_agents = []
        
        #calculate episilon based on episode
        #epsilon = 1 / i_episode
        ####### tweak episilon to get better results #######
        self.epsilon = 1.0/((episode_number/8000)+1)

        
        # Place wall agents
        for i in range(len(self.wallLocations)):
            a = WallAgent(self.id_count, self)
            self.id_count += 1
            self.schedule.add(a)
            #print("placing ", a, " at ", self.corralLocations[i])
            self.grid.place_agent(a, self.wallLocations[i])
            
        # Place random agents
        for i in range(self.number_random_agents):
            a = RandomAgent(self.id_count, self)
            self.id_count += 1
            self.schedule.add(a)
            cell_location = self.grid.find_empty()
            self.grid.place_agent(a, cell_location)
            
        # Place cow agents
        for i in range(self.number_cow_agents):
            c = CowAgent(self.id_count, self)
            self.id_count += 1
            self.schedule.add(c)
            #self.cow_agent_list.append(c) #make a list of cows
            cell_location = self.grid.find_empty()
            self.grid.place_agent(c, cell_location)

        # Place plan agents
        for i in range(self.number_plan_agents):
            p = PlanAgent(self.id_count, self)
            self.id_count += 1
            self.schedule.add(p)
            cell_location = self.grid.find_empty()
            self.grid.place_agent(p, cell_location)
            
        # Place monte carlo agents
        for i in range(self.number_monte_carlo_agents):
            m = MonteCarloAgent(self.id_count, self, self.Q_values[i], self.epsilon) # init MC agents with previous Q tables
            self.mc_agents.append(m) # save MC agents to retrieve Q values
            self.id_count += 1
            self.schedule.add(m)
            cell_location = self.grid.find_empty()
            self.grid.place_agent(m, cell_location)
            
        # Place TD agents
        for i in range(self.number_td_agents):
            t = TDAgent(self.id_count, self)
            self.id_count += 1
            self.schedule.add(t)
            cell_location = self.grid.find_empty()
            self.grid.place_agent(t, cell_location)
            

            
    def step(self):
        self.state = rl_methods.encode_state(self.grid)
        self.schedule.step()
        self.update_score()
        
        #print(np.matrix(self.state))
        #print("the current score is ", self.score)
        
        # Update rewards of Monte Carlo agents
        for mcagent in self.mc_agents:
            mcagent.update_rewards()

##        if self.schedule.time < self.max_timesteps:
##            self.schedule.step()
##            self.update_score()
##            #print("the current step is ", self.schedule.time)
##            print(np.matrix(self.state))
##            print("the current score is ", self.score)
##            self.datacollector.collect(self)
##        else:
##            print("the final score is ", self.score)

    def update_score(self):
        self.current_cow_count = cow_methods.cows_in_goal(self, self.goalState)
        self.total_cow_count += self.current_cow_count
        print(self.total_cow_count, self.current_cow_count, self.schedule.time)
        self.score = self.total_cow_count / self.schedule.time
        
    def get_new_Q_values(self):
        """ Update model Q values at the end of the episode, called by run after each episode """
        new_Q = []
        for agent in self.mc_agents:
            updated_Q = agent.Q_table_update()
            new_Q.append(copy.deepcopy(updated_Q))
        return new_Q
    

        
