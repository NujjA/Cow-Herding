import numpy as np

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
UP_LEFT = 4
UP_RIGHT = 5
DOWN_LEFT = 6
DOWN_RIGHT = 7
STAY = 8

action_space = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT, STAY]

def possible_action_space(agent, grid):
    possible_actions = [STAY]
    
    up_cell = grid.torus_adj((agent.pos[0]+1, agent.pos[1]))
    down_cell = grid.torus_adj((agent.pos[0]-1, agent.pos[1]))
    left_cell = grid.torus_adj((agent.pos[0], agent.pos[1]-1))
    right_cell = grid.torus_adj((agent.pos[0], agent.pos[1]+1))
    ul_cell = grid.torus_adj((agent.pos[0]+1, agent.pos[1]-1))
    dl_cell = grid.torus_adj((agent.pos[0]-1, agent.pos[1]-1))
    ur_cell = grid.torus_adj((agent.pos[0]+1, agent.pos[1]+1))
    dr_cell = grid.torus_adj((agent.pos[0]-1, agent.pos[1]+1))
    
    if grid.is_cell_empty(up_cell):
        possible_actions.append(UP)
    if grid.is_cell_empty(down_cell):
        possible_actions.append(DOWN)
    if grid.is_cell_empty(left_cell):
        possible_actions.append(LEFT)
    if grid.is_cell_empty(right_cell):
        possible_actions.append(RIGHT)
    if grid.is_cell_empty(ul_cell):
        possible_actions.append(UP_LEFT)
    if grid.is_cell_empty(dl_cell):
        possible_actions.append(DOWN_LEFT)
    if grid.is_cell_empty(ur_cell):
        possible_actions.append(UP_RIGHT)
    if grid.is_cell_empty(dr_cell):
        possible_actions.append(DOWN_RIGHT)
        
    return possible_actions


def encode_state(grid):
    
    state = np.zeros((grid.width, grid.height))
    for cell in grid.coord_iter():
        cell_content, x, y = cell
        if cell_content:
            #print(cell_content, x, y)
            #state[x][y] = encode_cell(cell_content)
            state[y][x] = encode_cell(cell_content) 
        
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
