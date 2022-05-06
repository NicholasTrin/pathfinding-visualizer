class Cell:
    def __init__(self, coordinate, g, h, f):
        self.coordinate = coordinate
        self.g = g
        self.h = h
        self.f = f

    def get_cardinal_moves(self):
        column, row = self.coordinate
        north = (column, row - 1)
        south = (column, row + 1)
        west = (column - 1, row)
        east = (column + 1, row)
        return [north, south, east, west]
