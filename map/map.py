import numpy as np
from .map_constants import *


class Map:

    def __init__(self, map_height, map_width, weights):
        self.map_height = map_height
        self.map_width = map_width
        self.map_units = None
        self.weights = weights
        self.map = None
        self.generate_map()

    def generate_map(self):
        self.map_units = self.map_width * self.map_height
        _map = None
        while self.check_map_validity(_map) is False:
            _map = np.random.choice([SPACE, WALL, WATER, MOUNTAIN], size=self.map_units, p=self.weights)
        self.map = _map

    def check_map_validity(self, _map) -> bool:
        if _map is None or _map[0] == WALL or _map[self.map_units - 1] == WALL:
            return False
        else:
            return True

    def get_movement_cost(self, coordinate):
        coordinate = self.get_two_to_one_dimensional_coordinates(coordinate)
        if self.map[coordinate] == SPACE:
            return SPACE_C
        elif self.map[coordinate] == WATER:
            return WATER_C
        elif self.map[coordinate] == MOUNTAIN:
            return MOUNTAIN_C

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
