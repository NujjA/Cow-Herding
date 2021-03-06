from mesa.space import SingleGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from wall import WallAgent
from random_agent import RandomAgent
from plan_agent import PlanAgent
from cow_agent import CowAgent
from montecarlo import MonteCarloAgent
from trained_mc_agent import TrainedMonteCarloAgent
from td_agent import TDAgent
import cow_methods
import numpy as np
import rl_methods
from movement_control import compute_score
import copy
from collections import defaultdict
import dill


class CHModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, height, random_n = 0, cow_n = 0, plan_n = 0, mc_n = 0, td_n = 0, episode_number = 0, t_mc_n = 0, old_Q_values = None):
        self.running = True 
        #self.num_agents = N
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        
        self.id_count = 0 #to assign each agent a unique ID
        #self.max_timesteps = 500 #max timesteps for each episode
        
        # To keep score
        self.total_cow_count = 0.0
        self.current_cow_count = 0.0
        self.score = 0.0
        self.previous_cow_count = 0.0
        
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
        self.number_trained_mc_agents = t_mc_n
        
        
        # load pre-trained data to add to or make new Q tables for MC Agents
        # set to false to make a new Q table
        #loadpretrained = True
        #if (loadpretrained and (not old_Q_values)):
        #    print("loading pkl file")
        #    with open('mc_q_save.pkl', 'rb') as file:
        #        self.Q_values = dill.load(file)
        
        
        # Monte Carlo Agent model save
        self.Q_table_sharing = True ## If true, agents share a Q table
        self.vision_range = 2 # How far the MC agents can see
        
        if old_Q_values: #load previous Q tables if they exist
            self.Q_values = old_Q_values
        else:
            self.Q_values = [] #no previous Q tables, so make new ones
            if (self.Q_table_sharing):
                # Just one Q table  
                self.Q_values.append(defaultdict(lambda: np.zeros(len(rl_methods.action_space))))
            else:
                #every agent gets it's own Q table
                for agent in range(self.number_monte_carlo_agents):
                    self.Q_values.append(defaultdict(lambda: np.zeros(len(rl_methods.action_space))))
        self.mc_agents = []
        
        self.episode = episode_number
        #calculate episilon based on episode
        #epsilon = 1 / i_episode
        ####### tweak episilon to get better results #######
        self.epsilon = 1.0/((episode_number/800) + 1)
        #self.epsilon = 1.0/((episode_number/8000)+1)

        
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
            Q_table_to_use = None
            if (self.Q_table_sharing): # If sharing Q tables, everyone gets a copy of the same Q table 
                Q_table_to_use = self.Q_values[0]
            else:
                Q_table_to_use = self.Q_values[i] # If not sharing, everyone gets a different Q table
            m = MonteCarloAgent(self.id_count, self, Q_table_to_use, self.epsilon, vision = self.vision_range) # init MC agents with previous Q tables
            self.mc_agents.append(m) # save MC agents to retrieve Q values
            self.id_count += 1
            self.schedule.add(m)
            cell_location = self.grid.find_empty()
            self.grid.place_agent(m, cell_location)
        
        # Place trained monte carlo agents
        # open/load trained Q table
        if (self.number_trained_mc_agents > 0):
            loaded_Q = None
            with open('mc_q_save.pkl', 'rb') as file:
                loaded_Q = dill.load(file)
            if loaded_Q:
                for i in range(self.number_trained_mc_agents):
                    tm = TrainedMonteCarloAgent(self.id_count, self, loaded_Q, vision = self.vision_range)
                    self.id_count += 1
                    self.schedule.add(tm)
                    cell_location = self.grid.find_empty()
                    self.grid.place_agent(tm, cell_location)
            else:
                print("Can't load Q table for trained MC Agents")
            
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
        
        rewards_type = 3
        # if rewards_type is 
        ###1 use the actual current score
        ###2 use number of cows in goal
        ###3 cows in goal with penalty if cow leaves goal
        
        # how penalized do you want the agents to be for letting cow escape?
        penalty_modifier = 0.0
        # how much of a bonus for getting cows to go in the goal?
        bonus_modifier = 100.0
        # bonus for keeping cows in goal
        bonus_cows = 5.0
        
        for mcagent in self.mc_agents:
            if (rewards_type == 1):
                mcagent.update_rewards(self.score)
            elif (rewards_type == 2):
                mcagent.update_rewards(self.current_cow_count)
            elif (rewards_type == 3):
                penalty = 0.0
                bonus = 0.0
                no_cow_penalty = -1.0
                if (self.current_cow_count < self.previous_cow_count):
                    print("calculating penalty ESCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPE")
                    cows_escaped = (float(self.previous_cow_count) - float(self.current_cow_count))
                    #print("this many escaped: ", cows_escaped, ", modifier: ", penalty_modifier)
                    penalty = penalty_modifier * cows_escaped
                    #print("prev cows ", self.previous_cow_count,  ", cows ", self.current_cow_count,  ", penalty ", penalty)
                if (self.current_cow_count > self.previous_cow_count):
                    print("calculating penalty COWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
                    cows_gained = (float(self.current_cow_count) - float(self.previous_cow_count))
                    #print("this many escaped: ", cows_escaped, ", modifier: ", penalty_modifier)
                    bonus = bonus_modifier * cows_gained
                if (self.current_cow_count < self.number_cow_agents):
                    penalty = penalty - (no_cow_penalty * (float(self.number_cow_agents) - float(self.current_cow_count)))
                mcagent.update_rewards((self.current_cow_count * bonus_cows) - penalty + bonus)
                print("current cow count: ", self.current_cow_count, ", penalty: ", penalty, ", bonus: ", bonus, ", no cow ")
                print("total reward: ", (self.current_cow_count * bonus_cows) - penalty + bonus)
            else:
                printing("using default reward")
                mcagent.update_rewards(self.score)

    def update_score(self):
        self.previous_cow_count = self.current_cow_count
        self.current_cow_count = cow_methods.cows_in_goal(self, self.goalState)
        self.total_cow_count += self.current_cow_count
        print(self.total_cow_count, self.current_cow_count, self.schedule.time, " Episode: ", self.episode)
        self.score = self.total_cow_count / self.schedule.time
        
    def get_new_Q_values(self):
        """ Update model Q values at the end of the episode, called by run after each episode """
        new_Q = []
        
        if(self.Q_table_sharing): #If all agents are sharing Q table data
            updated_Q = None
            for agent in self.mc_agents:
                # Update the Q table then pass it on to the next agent on the team to update
                updated_Q = agent.Q_table_update(shared_Q_table = updated_Q) 
            new_Q.append(copy.deepcopy(updated_Q))
        else:
            # If all agents have their own Q tables, update and save for next episode
            for agent in self.mc_agents:
                updated_Q = agent.Q_table_update()
                new_Q.append(copy.deepcopy(updated_Q))
        return new_Q
    

        
