from mesa import Agent, Model
import random

class WallAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
#        self.wealth = 1

 #   def move(self):
 #       possible_steps = self.model.grid.get_neighborhood(
 #           self.pos,
 #           moore=True,
 #           include_center=False)
 #       new_position = random.choice(possible_steps)
 #       self.model.grid.move_agent(self, new_position)

 #   def give_money(self):
 #       cellmates = self.model.grid.get_cell_list_contents([self.pos])
 #       if len(cellmates) > 1:
 #           other = random.choice(cellmates)
 #           other.wealth += 1
 #           self.wealth -= 1

    def step(self):
        """ Wall agents do not move """
        pass
#        self.move()
#        if self.wealth > 0:
#            self.give_money()
