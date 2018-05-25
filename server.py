from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import CHModel
from random_agent import RandomAgent
from wall import WallAgent
from cow_agent import CowAgent
from plan_agent import PlanAgent
import random

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

    return portrayal

grid = CanvasGrid(agent_portrayal, 8, 8, 500, 500)
server = ModularServer(CHModel,
                       [grid],
                       "Cow Herding Model",
                       {"N": 14, "width": 8, "height": 8})
