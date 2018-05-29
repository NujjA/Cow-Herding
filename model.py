from mesa.space import SingleGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from wall import WallAgent
from random_agent import RandomAgent
from plan_agent import PlanAgent
from cow_agent import CowAgent
import cow_methods

class CHModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.running = True 
        self.num_agents = N
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        
        self.id_count = 0 #to assign each agent a unique ID
        
        # To keep score
        self.total_cow_count = 0.0
        self.score = 0.0
        #self.cow_agent_list = []
        
        # Save model for agent use
        self.wallLocations = [(1,5), (1,6), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (6,6), (6,5)]
        self.goalState = [(2,5), (3,5), (4,5), (5,5), (2,6), (3,6), (4,6), (5,6)]
        self.goalTarget = (3,5) #corral "entrance" that plan agents herd towards
        
        self.number_random_agents = 2
        self.number_cow_agents = 4
        self.number_plan_agents = 2
        
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
            
    def step(self):
        self.schedule.step()
        self.update_score()
        #print("the current step is ", self.schedule.time)
        print("the current score is ", self.score)

    def update_score(self):
        current_cows = cow_methods.cows_in_goal(self, self.goalState)
        self.total_cow_count += current_cows
        self.score = self.total_cow_count / self.schedule.time
        
        
