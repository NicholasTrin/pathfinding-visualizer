from cell import Cell
from map_constants import *


class AStarSearch:

    def __init__(self, map):
        self.start = (0, 0)
        self.goal = (map.map_width - 1, map.map_height - 1)
        self.reached_goal = False
        self.map_width = map.map_width
        self.map_height = map.map_height
        self.map = map.map
        self.traversal_path = self.search()
        self.shortest_path = self.get_shortest_path(self.traversal_path)

    def search(self) -> list:
        open = [self.get_cell(self.start)]
        closed = []
        visited = set()
        while len(open) > 0:
            q = open[0]
            for cell in open:
                if cell.f < q.f:
                    q = cell
            open.remove(q)
            closed.append(q)
            if self.is_goal(q.coordinate):
                return closed
            for coordinate in self.get_successors(q.coordinate):
                successor = self.get_cell(coordinate, q)
                if coordinate not in visited:
                    visited.add(coordinate)
                    open.append(successor)
        return closed

    def get_shortest_path(self, evaluated_cells) -> list:
        def is_cardinal_move() -> bool:
            x, y = shortest_path[-1].coordinate
            north = (x, y - 1)
            south = (x, y + 1)
            west = (x - 1, y)
            east = (x + 1, y)
            if cell.coordinate in [north, south, east, west]:
                return True
            else:
                return False

        evaluated_cells = sorted(evaluated_cells, key=lambda cell: cell.g, reverse=True)
        shortest_path = [evaluated_cells[0]]
        for cell in evaluated_cells:
            if cell.g < shortest_path[-1].g and is_cardinal_move():
                shortest_path.append(cell)
        return reversed(shortest_path)

    def get_cell(self, coordinate, q=None) -> Cell:
        if q:
            g = q.g + self.get_movement_cost(coordinate)
        else:
            g = 0
        h = self.get_manhattan_distance(coordinate, self.goal)
        f = g + h
        return Cell(coordinate, g, h, f)

    def get_movement_cost(self, coordinate):
        row, column = coordinate
        if self.map[row * self.map_width + column] == WATER:
            return 2
        elif self.map[row * self.map_width + column] == SPACE:
            return 1

    def get_successors(self, coordinate) -> list:
        x, y = coordinate
        north = (x, y - 1)
        south = (x, y + 1)
        west = (x - 1, y)
        east = (x + 1, y)
        cardinal_moves = [north, south, west, east]
        for move in list(cardinal_moves):
            if not self.is_valid_move(move):
                cardinal_moves.remove(move)
        return cardinal_moves

    def is_valid_move(self, coordinate) -> bool:
        if 0 <= coordinate[0] < self.map_width and 0 <= coordinate[1] < self.map_height:
            if self.map[self.get_two_to_one_dimensional_coordinates(coordinate)] == WALL:
                return False
            else:
                return True
        else:
            return False

    def is_goal(self, coordinate) -> bool:
        if coordinate == self.goal:
            self.reached_goal = True
            return True
        else:
            return False

    def get_manhattan_distance(self, start, finish) -> int:
        return abs(start[0] - finish[0]) + abs(start[1] - finish[1])

    def get_two_to_one_dimensional_coordinates(self, coordinates) -> int:
        return coordinates[0] * self.map_width + coordinates[1]

    def get_one_to_two_dimensional_coordinates(self, coordinates) -> list:
        return [coordinates // self.map_width, coordinates % self.map_width]
