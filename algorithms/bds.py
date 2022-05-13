from .algorithmTemplate import *


class BDS(AlgorithmTemplate):

    def __init__(self, _map):
        super().__init__(_map)
        self.traversal_path = []
        self.shortest_path = self.search()

    def search(self) -> list:
        to_traverse = [[self.get_cell(self.start)]]
        visited = set()
        while len(to_traverse):
            current_path = to_traverse.pop(0)
            evaluate_cell = current_path[-1]
            self.traversal_path.append(evaluate_cell)
            if self.is_goal(evaluate_cell):
                return current_path
            for move in self.get_successors(evaluate_cell):
                if move not in visited:
                    new_path = current_path + [self.get_cell(move)]
                    visited.add(move)
                    to_traverse.append(new_path)

    def get_cell(self, coordinate, previous_cell=None):
        return Cell(coordinate,'-','-','-')

