from mesa.space import SingleGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from wall import WallAgent
from random_agent import RandomAgent

class CHModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.running = True 
        self.num_agents = N
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        self.corralLocations = [(1,5), (1,6), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (6,6), (6,5)]
        
        self.number_random_agents = 2
        
        # Place wall agents
        for i in range(len(self.corralLocations)):
            a = WallAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            #x = random.randrange(self.grid.width)
            #y = random.randrange(self.grid.height)
            print("placing ", a, " at ", self.corralLocations[i])
            self.grid.place_agent(a, self.corralLocations[i])
            
        # Place random agents
        for i in range(self.number_random_agents):
            a = RandomAgent(i, self)
            self.schedule.add(a)
            cell_location = self.grid.find_empty()
            self.grid.place_agent(a, cell_location)


    def step(self):
        self.schedule.step()
