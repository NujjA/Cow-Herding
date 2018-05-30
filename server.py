from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import CHModel
from random_agent import RandomAgent
from wall import WallAgent
from cow_agent import CowAgent
from plan_agent import PlanAgent
from montecarlo import MonteCarloAgent
from td_agent import TDAgent
import random
import movement_control

def agent_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {"Filled": "true"}
    
    if type(agent) is WallAgent:
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 0
        portrayal["Color"] = "red"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
    
    elif type(agent) is RandomAgent:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["Color"] = "blue"
        portrayal["r"] = .5
        
    elif type(agent) is CowAgent:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["Color"] = "black"
        portrayal["r"] = .5
    
    elif type(agent) is PlanAgent:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["Color"] = "purple"
        portrayal["r"] = .5

    elif type(agent) is MonteCarloAgent:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["Color"] = "green"
        portrayal["r"] = .5
        
    elif type(agent) is TDAgent:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["Color"] = "orange"
        portrayal["r"] = .5

    return portrayal

random_agents = 1
cow_agents = 4
plan_agents = 0
monte_carlo_agents = 1
td_agents = 0
grid = CanvasGrid(agent_portrayal, 8, 8, 500, 500)

nA = len(movement_control.possible_action_space)

# Starting with new Q tables. Replace here for saved Q tables.
MC_Q_values = [] 
for agent in range(monte_carlo_agents):
    MC_Q_values.append(defaultdict(lambda: np.zeros(nA)))

server = ModularServer(CHModel,
                       [grid],
                       "Cow Herding Model",
                       {"width": 8, "height": 8})
                       # TODO: random_n = random_agents, cow_n = cow_agents, plan_n = plan_agents, mc_n = monte_carlo_agents, td_n = td_agents, episode_number = episode, old_Q_values = MC_Q_values)
