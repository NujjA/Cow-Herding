from mesa import Agent, Model
import random

def find_empty_location(position, model):
    """ returns a list of surrounding empty locations steps """
    all_cells = model.grid.get_neighborhood(position, moore=True, include_center=True)
    empty_cells = []
    for cell in all_cells:
        if model.grid.is_cell_empty(cell):
            empty_cells.append(cell)
    return empty_cells
