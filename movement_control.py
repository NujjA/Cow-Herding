from mesa import Agent, Model
import random
import numpy as np

def find_empty_location(position, model):
    """ returns a list of surrounding empty locations steps """
    all_cells = model.grid.get_neighborhood(position, moore=True, include_center=True)
    empty_cells = []
    for cell in all_cells:
        if model.grid.is_cell_empty(cell):
            empty_cells.append(cell)
    return empty_cells

def get_distance(grid, pos_1, pos_2):
        """ Get the distance between two point, accounting for toroidal space.
        Args:
            pos_1, pos_2: Coordinate tuples for both points.
            
        adapted from Mesa space.ContinuousSpace
        """
        x1, y1 = pos_1
        x2, y2 = pos_2

        dx = np.abs(x1 - x2)
        dy = np.abs(y1 - y2)

        #looping grid
        dx = min(dx, grid.width - dx)
        dy = min(dy, grid.height - dy)

        return np.sqrt(dx * dx + dy * dy)
