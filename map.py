import numpy as np
from map_constants import *


class Map:

    def __init__(self, map_height=10, map_width=20, weights=[0.5, 0.25, 0.15,0.10]):
        self.map_height = map_height
        self.map_width = map_width
        self.map_units = map_width * map_height
        self.space_to_wall_weights = weights
        self.map = None
        self.generate_map()

    def generate_map(self) -> list:
        while self.check_map_validity() is False:
            self.map = np.random.choice([SPACE, WALL, WATER, MOUNTAIN], size=self.map_units, p=self.space_to_wall_weights)

    def check_map_validity(self) -> bool:
        if self.map is None or self.map[0] == WALL or self.map[self.map_units - 1] == WALL:
            return False
        else:
            return True

    def get_movement_cost(self, coordinate):
        coordinate = self.get_two_to_one_dimensional_coordinates(coordinate)
        if self.map[coordinate] == SPACE:
            return 1
        elif self.map[coordinate] == WATER:
            return 2
        elif self.map[coordinate] == MOUNTAIN:
            return 3

    def is_valid_move(self, coordinate) -> bool:
        if 0 <= coordinate[0] < self.map_width and 0 <= coordinate[1] < self.map_height:
            if self.map[self.get_two_to_one_dimensional_coordinates(coordinate)] == WALL:
                return False
            else:
                return True
        else:
            return False

    def get_two_to_one_dimensional_coordinates(self, coordinates) -> int:
        column, row = coordinates
        return column + row * self.map_width

    def get_one_to_two_dimensional_coordinates(self, coordinates) -> list:
        return [coordinates // self.map_width, coordinates % self.map_width]
