from mesa import Agent, Model
import random
import movement_control, cow_methods
import numpy as np

class PlanAgent(Agent):
    """ An agent that follows plan of JIAC V team by Heβler et al. (2010) """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print("creating plan agent")
        
        self.need_new_action = True #finished current task, find a new action
        
        # plan steps
        # look for cloeset cow to goal
        self.LOOKFORCOW = 0
        # “HERD_TOWARDS_GOAL”: The agent moves a particular cow towards the agent’s team corral. This can be by pushing or following. Following a cow moves it in the opposite direction from the agent since the cow algorithm assigns a large negative weight to agents.
        self.HERDCOW = 1
        # “HERD_TOGETHER”: The agent moves a particular cow towards another cow. This can be by pushing or following. Following a cow moves it in the opposite direction from the agent since the cow algorithm assigns a large negative weight to agents.
        self.HERDTOGETHER = 2
        # “FLANK”: The agent moves around a group of one or more cows, staying a specified distance away.
        self.FLANK = 3
        # “HEAD_TOWARDS_COW”: The agent moves towards a particular cow.
        self.TOWARDSCOW = 4
        # “BLOCK”: The agent locates itself directly outside the entrance to the goal to act as a barrier.
        self.BLOCK = 5
        # “HEAD_TOWARDS_GOAL”: Go towards goal 
        self.TOWARDSGOAL = 6
        
        
        
        
        self.vision_radius = 3 # How far the agent can see
        
        self.current_plan_step = 0
        self.cow_to_follow = None
        self.cow_to_herd_towards = None

    def step(self):
        print("plan agent step")
        self.move()

    def move(self):
        if(self.need_new_action): 
            possible_actions = [self.BLOCK]
            # decide possible actions
            # if not at the goal space
            if(not((self.pos[0] == self.model.goalTarget[0]) and (self.pos[1] == self.model.goalTarget[1]))):
                possible_actions.append(self.TOWARDSGOAL)

            # if have a target cow and more than one cow in the radius
            neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center=False, radius= self.vision_radius)
            cows_in_radius = cow_methods.find_neighbor_cows(neighbors)
            if(self.cow_to_follow and (len(cows_in_radius) > 0)):
                possible_actions.append(self.HERDTOGETHER)
                
            # if have a target cow, can head towards it, flank it, or herd it towards the goal
            if(self.cow_to_follow):
                possible_actions.extend(self.TOWARDSCOW, self.FLANK, self.HERDCOW)
            else: #no cow to follow, find one
                possible_actions.append(self.LOOKFORCOW)
        
            # Choose an action
            print("possible actions are ", possible_actions)
            self.current_plan_step = random.choice(possible_actions)
        
        if (self.current_plan_step == self.LOOKFORCOW): # Find a cow
            print("finding cow to follow")
            self.cow_to_follow = self.find_free_cow_in_radius()
            if (self.cow_to_follow is not None):
                print("found cow")
                #self.current_plan_step = self.HERDCOW
                self.need_new_action = True
            else:
                # Move randomly to find a cow
                print("no cow here, keep looking")
                possible_steps = movement_control.find_empty_location(self.pos, self.model)
                new_position = random.choice(possible_steps)
                self.model.grid.move_agent(self, new_position)
        elif (self.current_plan_step == self.HERDCOW): # herd a cow towards the goal
            print("herding cow to goal")
            if not self.cow_to_follow: # if no cow to follow
                #self.current_plan_step = self.LOOKFORCOW
                self.need_new_action = True
            elif self.cow_to_follow.pos in self.model.goalState: # cow is already in goal
                print("cow is in the goal - resetting")
                #self.current_plan_step = self.LOOKFORCOW
                self.cow_to_follow = None
                self.need_new_action = True
            else:
                # herd the cow
                print("herding cow")
                self.move_to_herding_location()
        elif (self.current_plan_step == self.FLANK):
            print("flanking cow")
            if not self.cow_to_follow: # if no cow to follow
                print("no cow to flank")
                self.need_new_action = True
            if (random.randint(0, 4) == 0): # don't want to flank forever
                print("not flanking anymore")
                self.need_new_action = True
            else:
                self.flank_cow()

        elif (self.current_plan_step == self.HERDTOGETHER):
            print("herding cows together")
            if not self.cow_to_follow: # if no cow to follow
                print("no cow to herd")
                self.need_new_action = True
            elif not self.cow_to_herd_towards:
                print("CHOOSE SECONDARY COW")
                self.choose_secondary_cow()
                self.herd_cows_together()
            else:
                self.herd_cows_together()
        elif (self.current_plan_step == self.TOWARDSCOW): #take a step towards a cow
            print("one step towards cow")
            if not self.cow_to_follow: # if no cow to follow
                self.need_new_action = True
            else:
                movement_control.move_towards(self, self.cow_to_follow.pos)
                self.need_new_action = True

        elif (self.current_plan_step == self.BLOCK):
            # don't want to block forever, chance to break out of block
            if (random.randint(0, 4) == 0):
                print("not blocking anymore")
                self.need_new_action = True
            else:
                print("block")
                self.block()
                
        elif (self.current_plan_step == self.TOWARDSGOAL):
            # if not at the goal space
            if((self.pos[0] == self.model.goalTarget[0]) and (self.pos[1] == self.model.goalTarget[1])):
               print("already at goal")
               self.need_new_action = True
            else:
                print("moving towards goal")
                movement_control.move_towards(self, self.model.goalTarget)
        else:
            print("No more available actions, choose again")
            self.need_new_action = True
            
    def block(self):
        print("in block method")
        distance = movement_control.get_distance(grid, self.pos, self.model.goalTarget)
        if (float(distance) > (float(self.vision_radius) / 2.0)) :
            print("moving to block")
            movement_control.move_towards(self, self.cow_to_follow.pos)
        
    def flank_cow(self):
        print("in flank method")
        # if distance from me to the cow is greater than half the vision range
        distance = movement_control.get_distance(grid, self.pos, self.cow_to_follow.pos)
        if (float(distance) > (float(self.vision_radius) / 2.0)) :
            print("moving to flank")
            movement_control.move_towards(self, self.cow_to_follow.pos)
        
    def choose_secondary_cow(self):
        print("choosing secondary cow")
        neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center=False, radius= self.vision_radius)
        cows_in_radius = cow_methods.find_neighbor_cows(neighbors)
        free_cows = []
        for cow in cows_in_radius:
            if cow not in self.model.goalState:
                if (cow != self.cow_to_follow):
                    free_cows.append(cow)
        if(len(free_cows) > 0):
            print("cow chosen")
            return random.choice(free_cows)
        else:
            print("cow not chosen")
            return None

        
    def herd_cows_together(self):
        if not self.cow_to_follow:
            self.need_new_action = True # no cow to follow
        elif not self.cow_to_herd_towards:
            self.need_new_action = True # no cow to herd towards
        else:
                
            target_pos = None
            goal_pos = self.cow_to_herd_towards.pos # for clarity when reading code
            cow_pos = self.cow_to_follow.pos # for clarity when reading code
            
            if((goal_pos[0] == cow_pos[0]) or (goal_pos[1] == cow_pos[1])): #if the cows are adjacent vert or horiz, a chance to stop herding next round
                if (random.randint(0, 4) == 0):
                    self.need_new_action = True
                    self.cow_to_follow = None
                    self.cow_to_herd_towards = None

            #if goal is greater y than cow
            if movement_control.is_greater_y(goal_pos, cow_pos):
                target_pos = (cow_pos[0], cow_pos[1]-1)

            #if goal is smaller y than cow
            elif movement_control.is_smaller_y(goal_pos, cow_pos):
                target_pos = (cow_pos[0], cow_pos[1]+1)
            
            #if goal is greater x than cow
            elif movement_control.is_greater_x(goal_pos, cow_pos):
                target_pos = (cow_pos[0]-1, cow_pos[1])

            #if goal is smaller x than cow
            elif movement_control.is_smaller_x(goal_pos, cow_pos):
                target_pos = (cow_pos[0]+1, cow_pos[1])
            
            if target_pos:
                target_pos = self.model.grid.torus_adj(target_pos)
                movement_control.move_towards(self, target_pos)
                print("herding cow, new position: ", target_pos)
        
        
    def move_to_herding_location(self):
        target_pos = None
        goal_pos = self.model.goalTarget # for clarity when reading code
        cow_pos = self.cow_to_follow.pos # for clarity when reading code
        
        #if goal is greater y than cow
        if movement_control.is_greater_y(goal_pos, cow_pos):
            target_pos = (cow_pos[0], cow_pos[1]-1)

        #if goal is smaller y than cow
        elif movement_control.is_smaller_y(goal_pos, cow_pos):
            target_pos = (cow_pos[0], cow_pos[1]+1)
            
        #if goal is greater x than cow
        elif movement_control.is_greater_x(goal_pos, cow_pos):
            target_pos = (cow_pos[0]-1, cow_pos[1])

        #if goal is smaller x than cow
        elif movement_control.is_smaller_x(goal_pos, cow_pos):
            target_pos = (cow_pos[0]+1, cow_pos[1])
            
        if target_pos:
            target_pos = self.model.grid.torus_adj(target_pos)
            movement_control.move_towards(self, target_pos)
            
        print("moving towards ", target_pos)
        #self.pos
            
        
    def find_free_cow_in_radius(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center=False, radius= self.vision_radius)
        cows_in_radius = cow_methods.find_neighbor_cows(neighbors)
        free_cows = []
        for cow in cows_in_radius:
            if cow not in self.model.goalState:
                free_cows.append(cow)
        if(len(free_cows) > 0):
            return random.choice(free_cows)
        else:
            return None
        #return self.find_closest_cow_to_goal(free_cows)

        
    #def find_closest_cow_to_goal(self, free_cows):
    #    if not free_cows:
    #        return None
    #    
    #    closest_cow = None
    #    closest_distance = np.inf
    #    for cow in free_cows:
    #        current_distance = movement_control.get_distance(self.model.grid, cow.pos, self.model.goalTarget)
    #        if (current_distance < closest_distance):
    #            closest_distance = current_distance
    #            closest_cow = cow
    #    return closest_cow
