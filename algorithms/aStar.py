from cell import Cell

def get_manhattan_distance(start, finish) -> int:
    row1, column1 = start
    row2, colum2 = finish
    return abs(row1 - row2) + abs(column1 - colum2)


class AStarSearch:

    def __init__(self, map):
        self.start = (0, 0)
        self.goal = (map.map_width - 1, map.map_height - 1)
        self.reached_goal = False
        self.map_width = map.map_width
        self.map_height = map.map_height
        self.map = map
        self.traversal_path = self.search()
        self.shortest_path = self.get_shortest_path(self.traversal_path)

    def search(self) -> list:
        open = [self.get_cell(self.start)]
        closed = []
        visited = set()
        visited.add(self.start)
        while len(open) > 0:
            q = open[0]
            for cell in open:
                if cell.f < q.f:
                    q = cell
            open.remove(q)
            closed.append(q)
            if self.is_goal(q.coordinate):
                return closed
            for coordinate in self.get_successors(q):
                successor = self.get_cell(coordinate, q)
                if coordinate not in visited:
                    visited.add(coordinate)
                    open.append(successor)
        return closed

    def get_successors(self, cell) -> list:
        cardinal_moves = cell.get_cardinal_moves()
        for move in list(cardinal_moves):
            if not self.map.is_valid_move(move):
                cardinal_moves.remove(move)
        return cardinal_moves

    def get_cell(self, coordinate, q=None) -> Cell:
        if q:
            g = q.g + self.map.get_movement_cost(coordinate)
        else:
            g = 0
        h = get_manhattan_distance(coordinate, self.goal)
        f = g + h
        return Cell(coordinate, g, h, f)

    def is_goal(self, coordinate) -> bool:
        if coordinate == self.goal:
            self.reached_goal = True
            return True
        else:
            return False

    def get_shortest_path(self, evaluated_cells) -> list:
        def is_cardinal_move() -> bool:
            if cell.coordinate in shortest_path[-1].get_cardinal_moves():
                return True
            else:
                return False

        evaluated_cells = sorted(evaluated_cells, key=lambda cell: cell.g, reverse=True)
        shortest_path = [evaluated_cells[0]]
        for cell in evaluated_cells:
            if cell.g < shortest_path[-1].g and is_cardinal_move():
                shortest_path.append(cell)
            if cell.coordinate == self.start:
                break
        return reversed(shortest_path)

