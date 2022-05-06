from cell import Cell
from abc import ABC, abstractmethod


class AlgorithmTemplate(ABC):

    def __init__(self, _map):
        self.start = (0, 0)
        self.goal = (_map.map_width - 1, _map.map_height - 1)
        self.reached_goal = False
        self.map_width = _map.map_width
        self.map_height = _map.map_height
        self.map = _map

    def get_successors(self, cell) -> list:
        cardinal_moves = cell.get_cardinal_moves()
        for move in list(cardinal_moves):
            if not self.map.is_valid_move(move):
                cardinal_moves.remove(move)
        return cardinal_moves

    def is_goal(self, coordinate) -> bool:
        if coordinate == self.goal:
            self.reached_goal = True
            return True
        else:
            return False

    @abstractmethod
    def search(self, coordinate) -> list:
        pass

    @abstractmethod
    def get_cell(self, coordinate, q):
        pass

    @abstractmethod
    def get_shortest_path(self, evaluated_cells) -> list:
        pass
