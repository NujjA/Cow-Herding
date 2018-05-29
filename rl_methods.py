import numpy as np

def encode_state(grid):
    
    state = np.zeros((grid.width, grid.height))
    for cell in grid.coord_iter():
        cell_content, x, y = cell
        if cell_content:
            print(cell_content, x, y)
            state[x][y] = encode_cell(cell_content) 
        
    return state

def encode_cell(cell_item):
    if cell_item.__class__.__name__ is "WallAgent":
        return 1
    if cell_item.__class__.__name__ is "RandomAgent":
        return 2
    if cell_item.__class__.__name__ is "CowAgent":
        return 3
    if cell_item.__class__.__name__ is "PlanAgent":
        return 4
    if cell_item.__class__.__name__ is "MonteCarloAgent":
        return 5
    if cell_item.__class__.__name__ is "TDAgent":
        return 6

    return 0
