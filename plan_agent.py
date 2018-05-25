from mesa import Agent, Model
import random
import movement_control
import numpy as np

class PlanAgent(Agent):
    """ An agent that follows plan of JIAC V team by Heβler et al. (2010) """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print("creating plan agent")
        
        
        # plan steps
        # look for cloeset cow to goal
        self.LOOKFORCOW = 0
        # herd cow
        self.HERDCOW = 1
        
        self.current_plan_step = 0
        self.cow_to_follow = None

    def step(self):
        print("plan agent step")
        self.move()

    def move(self):
        #possible_steps = movement_control.find_empty_location(self.pos, self.model)
        #new_position = random.choice(possible_steps)
        #self.model.grid.move_agent(self, new_position)
        
        if (self.current_plan_step == self.LOOKFORCOW):
            print("finding cow to follow")
            self.find_cow_to_follow()
            if (self.cow_to_follow is not None):
                self.current_plan_step = self.HERDCOW
        elif (self.current_plan_step == self.HERDCOW):
            print("herding cow")
            
        
    def find_cow_to_follow(self):
        # get list of free cows
        free_cows = self.get_free_cow_list()
        # select closest to goal
        self.cow_to_follow = self.find_closest_cow_to_goal(free_cows)

    def get_free_cow_list(self):
        free_cows = []
        for cow in self.model.cow_agent_list:
            if cow.pos not in self.model.goalState:
                free_cows.append(cow)
        return free_cows
        
    def find_closest_cow_to_goal(self, free_cows):
        if not free_cows:
            return None
        
        closest_cow = None
        closest_distance = np.inf
        for cow in free_cows:
            current_distance = movement_control.get_distance(self.model.grid, cow.pos, self.model.goalTarget)
            if (current_distance < closest_distance):
                closest_distance = current_distance
                closest_cow = cow
        return closest_cow
