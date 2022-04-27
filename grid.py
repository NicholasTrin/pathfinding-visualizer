import time
from tkinter import *
from simulation import AStarSearch
from map import *


class Grid:

    def __init__(self, root, map_width=None, map_height=None):
        self.map = Map()
        self.map_width = self.map.map_width
        self.map_height = self.map.map_height
        self.cell_width = 30
        self.cell_height = 30

        self.simulation = AStarSearch(self.map)
        self.simulation_speed = 0

        self.pixel_height = 414
        self.pixel_width = 896

        self.squares = {}
        self.cost = {}
        self.show_data = {}

        self.root = root
        self.canvas = Canvas(root, height=self.pixel_height, width=self.pixel_width, bg='white')
        self.canvas.pack(fill=BOTH, expand=True)
        self.button_simulation = Button(self.root, command=self.run_simulation, text="Start Simulation")
        self.button_simulation.pack()
        self.button_reset_simulation = Button(self.root, command=self.reset_simulation, text="Reset Simulation")
        self.button_reset_simulation.pack()
        self.simulation_slider = Scale(root, from_=1, to=100, command=self.set_delay, orient=HORIZONTAL, length=600,
                                       tickinterval=25, label="Simulation Speed")
        self.simulation_slider.set(50)
        self.simulation_slider.pack()

        self.configure_grid()

    def set_delay(self, value):
        self.simulation_speed = float(value) / 100

    def configure_grid(self, event=None):
        for row in range(self.map_width):
            for column in range(self.map_height):
                x1 = column * self.cell_width
                y1 = row * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height
                if self.map.map[row * self.map_width + column] == WALL:
                    self.squares[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill='black', tags='rect')
                elif self.map.map[row * self.map_width + column] == WATER:
                    self.squares[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill='blue', tags='rect')
                else:
                    self.squares[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', tags='rect')
                self.cost[row, column] = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="-", fill='black',
                                                                 font='Helvetica 14 bold')
        self.show_data['shortest_path'] = self.canvas.create_text((self.map_width + 1) * self.cell_width + 15,
                                                                  self.cell_height, anchor=N, text="Shortest Path:",
                                                                  fill='black')
        self.show_data['reached_goal'] = self.canvas.create_text((self.map_width + 5) * self.cell_width + 15,
                                                                 self.cell_height, anchor=N, text="Reached Goal:",
                                                                 fill='black')

    def reset_simulation(self, event=None):
        self.canvas.delete('all')
        self.map = Map()
        self.squares = {}
        self.cost = {}
        self.show_data = {}
        self.simulation = AStarSearch(self.map)
        self.configure_grid()
        self.button_simulation.config(state=ACTIVE)

    def run_simulation(self, event=None):
        self.button_simulation.config(state=DISABLED)
        self.button_reset_simulation.config(state=DISABLED)
        for cell in self.simulation.traversal_path:
            row, column = cell.coordinate
            if self.map.map[row * self.map_width + column] == WATER:
                self.canvas.itemconfig(self.squares[row, column], fill='#6AFB92')
            else:
                self.canvas.itemconfig(self.squares[row, column], fill='#C04000')
            self.canvas.itemconfig(self.cost[row, column], fill='black', text=cell.g)
            self.canvas.update()
            time.sleep(self.simulation_speed)

        shortest_path_text = 'Shortest path:\n'
        for cell in self.simulation.shortest_path:
            shortest_path_text += str(cell.coordinate) + '\n'
            row, column = cell.coordinate
            x1 = column * self.cell_width
            y1 = row * self.cell_height
            x2 = x1 + self.cell_width
            y2 = y1 + self.cell_height
            self.canvas.create_line(x1, y1, x2, y2)
            self.canvas.update()
            time.sleep(self.simulation_speed)
        self.canvas.itemconfig(self.show_data['shortest_path'], text=shortest_path_text)
        self.canvas.itemconfig(self.show_data['reached_goal'],
                               text="Reached Goal: {}".format(self.simulation.reached_goal))
        self.button_reset_simulation.config(state=ACTIVE)
