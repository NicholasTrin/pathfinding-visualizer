import time
from tkinter import *
from tkinter import ttk
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
        self.simulation_data = {}
        self.buttons = {}
        self.scales = {}

        self.root = root
        self.canvas = Canvas(root, height=self.pixel_height, width=self.pixel_width, bg='white')
        self.canvas.pack(fill=BOTH, expand=True)

        self.configure_ui()
        self.configure_grid()

    def configure_ui(self):
        self.buttons['button_simulation'] = Button(self.root, command=self.run_simulation, text="Start Simulation")
        self.buttons['button_simulation'].pack()
        self.buttons['button_reset_simulation'] = Button(self.root, command=self.reset_simulation, text="Reset Simulation")
        self.buttons['button_reset_simulation'].pack()
        self.scales['simulation_speed'] = Scale(self.root, from_=0.1, to=100, command=self.set_delay, orient=HORIZONTAL, length=600,
                                       tickinterval=25, label="Simulation Speed")
        self.scales['simulation_speed'].set(50)
        self.scales['simulation_speed'].pack()

        self.simulation_data['attributes'] = ('Coordinate (X,Y)', 'F (Total Cost)', 'G (Movement Cost)', 'H (Heuristic)', 'Reached Goal?')
        self.simulation_data['shortest_path'] = ttk.Treeview(self.root)
        self.simulation_data['shortest_path']['columns'] = self.simulation_data['attributes']
        self.simulation_data['shortest_path'].column("#0", width=0, stretch=NO)
        self.simulation_data['shortest_path'].heading("#0", text='', anchor=N)
        for attribute in self.simulation_data['attributes']:
            self.simulation_data['shortest_path'].column(attribute, anchor=N,width=150)
            self.simulation_data['shortest_path'].heading(attribute, text=attribute, anchor=CENTER)
        self.simulation_data['shortest_path'].pack()

    def configure_grid(self, event=None):
        for column in range(self.map_width):
            for row in range(self.map_height):
                x1 = column * self.cell_width
                y1 = row * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height
                if self.map.map[column + row * self.map_width] == WALL:
                    self.squares[column, row] = self.canvas.create_rectangle(x1, y1, x2, y2, fill='black', tags='rect')
                elif self.map.map[column + row * self.map_width] == WATER:
                    self.squares[column, row] = self.canvas.create_rectangle(x1, y1, x2, y2, fill='blue', tags='rect')
                else:
                    self.squares[column, row] = self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', tags='rect')
                self.cost[column, row] = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="-", fill='black',
                                                                 font='Helvetica 14 bold')

    def reset_simulation(self, event=None):
        self.canvas.delete('all')
        self.map = Map()
        self.squares = {}
        self.cost = {}
        self.simulation = AStarSearch(self.map)
        self.simulation_data['shortest_path'].delete(*self.simulation_data['shortest_path'].get_children())
        self.configure_grid()
        self.buttons['button_simulation'].config(state=ACTIVE)

    def run_simulation(self, event=None):
        self.buttons['button_simulation'].config(state=DISABLED)
        self.buttons['button_reset_simulation'].config(state=DISABLED)
        for cell in self.simulation.traversal_path:
            column, row = cell.coordinate
            if self.map.map[column + row * self.map_width] == WATER:
                self.canvas.itemconfig(self.squares[column, row], fill='#6AFB92')
            else:
                self.canvas.itemconfig(self.squares[column, row], fill='#C04000')
            self.canvas.itemconfig(self.cost[column, row], fill='black', text=cell.g)
            self.canvas.update()
            time.sleep(self.simulation_speed)

        for cell in self.simulation.shortest_path:
            self.simulation_data['shortest_path'].insert(parent='',iid=cell.coordinate,index=END,values=(cell.coordinate,cell.f,cell.g,cell.h))
            column,row = cell.coordinate
            x1 = column * self.cell_width
            y1 = row * self.cell_height
            x2 = x1 + self.cell_width
            y2 = y1 + self.cell_height
            self.canvas.create_line(x1, y1, x2, y2)
            self.canvas.update()
            time.sleep(self.simulation_speed)
        self.simulation_data['shortest_path'].set(item=(0,0), column='Reached Goal?', value=str(self.simulation.reached_goal))
        self.buttons['button_reset_simulation'].config(state=ACTIVE)

    def set_delay(self, value):
        self.simulation_speed = float(value) / 100
