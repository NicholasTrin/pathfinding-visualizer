import numpy as np
from map_constants import *


class Map:

    def __init__(self, map_height=10, map_width=10, weights=[0.6, 0.25, 0.15]):
        self.map_height = 10
        self.map_width = 10
        self.map_units = map_width * map_height
        self.space_to_wall_weights = weights
        self.map = None
        self.generate_map()

    def generate_map(self) -> list:
        while self.check_map_validity() is False:
            self.map = np.random.choice([SPACE, WALL, WATER], size=self.map_units, p=self.space_to_wall_weights)

    def check_map_validity(self) -> bool:
        if self.map is None or self.map[0] == WALL or self.map[self.map_units - 1] == WALL:
            return False
        else:
            return True
