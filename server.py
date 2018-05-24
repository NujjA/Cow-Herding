from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import CHModel
from random_agent import RandomAgent
from wall import WallAgent
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
        

    return portrayal

grid = CanvasGrid(agent_portrayal, 8, 8, 500, 500)
server = ModularServer(CHModel,
                       [grid],
                       "Cow Herding Model",
                       {"N": 12, "width": 8, "height": 8})
