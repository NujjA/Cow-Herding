
# weights based on cows from Multi Agent Programming Contest
COWWEIGHT = 10.0;
EMPTYWEIGHT = 3.0;
CORRALWEIGHT = 3.0;
AGENTWEIGHT = -200.0;
OBSTACLEWEIGHT = -4.0;

def find_neighbor_cows(neighbors):
    cows_in_radius = []
    for neighbor in neighbors:
        if neighbor.__class__.__name__ is "CowAgent":
            cows_in_radius.append(neighbor)
    return cows_in_radius


def determine_weight(agent):
    weight = 0.0
    if agent.__class__.__name__ is "WallAgent":
        weight = OBSTACLEWEIGHT
    if agent.__class__.__name__ is "RandomAgent":
        weight = AGENTWEIGHT
    if agent.__class__.__name__ is "CowAgent":
        weight = COWWEIGHT
    if agent.__class__.__name__ is "PlanAgent":
        weight = AGENTWEIGHT
    if agent.__class__.__name__ is "MonteCarloAgent":
        weight = AGENTWEIGHT
    if agent.__class__.__name__ is "TDAgent":
        weight = AGENTWEIGHT
    return weight

def cows_in_goal(model, goalState):
    ''' The score of the current timestep '''
    cow_count = 0
    cell_contents = model.grid.get_cell_list_contents(goalState)
    print(cell_contents)
    if len(cell_contents) > 1:
        for agent in cell_contents:
            if agent.__class__.__name__ is "CowAgent":
                cow_count += 1
    return cow_count

