from mesa.space import SingleGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from wall import WallAgent
from random_agent import RandomAgent
from cow_agent import CowAgent

class CHModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.running = True 
        self.num_agents = N
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        self.id_count = 0 #to assign each agent a unique ID
        
        self.corralLocations = [(1,5), (1,6), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (6,6), (6,5)]
        
        self.number_random_agents = 2
        self.number_cow_agents = 2
        
        # Place wall agents
        for i in range(len(self.corralLocations)):
            a = WallAgent(self.id_count, self)
            self.id_count += 1
            self.schedule.add(a)
            #print("placing ", a, " at ", self.corralLocations[i])
            self.grid.place_agent(a, self.corralLocations[i])
            
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
            cell_location = self.grid.find_empty()
            self.grid.place_agent(c, cell_location)


    def step(self):
        for agent in self.schedule.agents:
            print(type(agent))
        self.schedule.step()
