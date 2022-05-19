import time
import tkinter
from tkinter import *
from tkinter import ttk
from algorithms import aStar, bds, dijkstra, dfs
from map.map import *


class Grid:

    def __init__(self, root):
        self.map_width = 30
        self.map_height = 10
        self.map_probabilities = [0.5, 0.25, 0.15, 0.10]
        self.map = Map(self.map_height, self.map_width, self.map_probabilities)
        self.cell_width = 30
        self.cell_height = 30

        self.algorithm = None
        self.simulation_speed = 0

        self.pixel_height = 800
        self.pixel_width = 896

        self.squares = {}
        self.cost = {}
        self.simulation_data = {}
        self.buttons = {}
        self.data_entry = {}
        self.scales = {}

        self.root = root
        self.canvas = Canvas(root, height=self.pixel_height, width=self.pixel_width, bg='white')
        self.canvas.pack(fill=BOTH, side=TOP, expand=True)

        self.configure_ui()
        self.configure_grid()

    def configure_ui(self):
        self.buttons['button_simulation'] = Button(self.root, command=self.run_simulation, text="Start Simulation")
        self.buttons['button_simulation'].pack()
        self.buttons['button_reset_simulation'] = Button(self.root, command=self.reset_simulation,
                                                         text="Reset Simulation")
        self.buttons['button_reset_simulation'].pack()
        self.scales['simulation_speed'] = Scale(self.root, from_=0.1, to=100, command=self.set_delay, orient=HORIZONTAL,
                                                length=600, tickinterval=25, label="Simulation Speed")
        self.scales['simulation_speed'].set(25)
        self.scales['simulation_speed'].pack()
        self.data_entry['algorithm_selection'] = Listbox(master=self.root, listvariable=tkinter.StringVar(
            value=('A*', 'Breadth First Search', 'Depth First Search', 'Dijkstra',)),
                                                         selectmode=SINGLE, height=5)
        self.data_entry['algorithm_selection'].select_set(0)
        self.data_entry['algorithm_selection'].bind("<<ListboxSelect>>", self.algorithm_selected)
        self.data_entry['algorithm_selection'].event_generate("<<ListboxSelect>>")
        self.data_entry['algorithm_selection'].pack()

        self.data_entry['width_label'] = Label(self.canvas, text='Map Width')
        self.data_entry['width_label'].pack(side=LEFT, anchor=S)
        self.data_entry['map_inputs_width'] = Entry(self.canvas, width=20)
        self.data_entry['map_inputs_width'].insert(END, '30')
        self.data_entry['map_inputs_width'].pack(side=LEFT, anchor=S)
        self.data_entry['height_label'] = Label(self.canvas, text='Map Height')
        self.data_entry['height_label'].pack(side=LEFT, anchor=S)
        self.data_entry['map_inputs_height'] = Entry(self.canvas, width=20)
        self.data_entry['map_inputs_height'].insert(END, '10')
        self.data_entry['map_inputs_height'].pack(side=LEFT, anchor=S)
        self.data_entry['probabilities_label'] = Label(self.canvas,
                                                       text='Tile Probabilities (Space, Wall, Water, Mountain)')
        self.data_entry['probabilities_label'].pack(side=LEFT, anchor=S)
        self.data_entry['map_inputs_probabilities'] = Entry(self.canvas, width=20)
        self.data_entry['map_inputs_probabilities'].insert(END, '0.5, 0.25, 0.15,0.10')
        self.data_entry['map_inputs_probabilities'].pack(side=LEFT, anchor=S)
        self.buttons['map_inputs'] = Button(self.canvas, text='Input Map Data', width=20, command=self.enter_map_data)
        self.buttons['map_inputs'].pack(side=LEFT, anchor=S)
        self.data_entry['error_string_var'] = StringVar()
        self.data_entry['error_string_var'].set('No errors.')
        self.data_entry['error_label'] = Label(self.canvas, textvariable=self.data_entry['error_string_var'])
        self.data_entry['error_label'].pack(side=LEFT, anchor=SW)

        self.simulation_data['attributes'] = (
            'Coordinate (X,Y)', 'F (Total Cost)', 'G (Movement Cost)', 'H (Heuristic)', 'Reached Goal?')
        self.simulation_data['shortest_path'] = ttk.Treeview(self.root)
        self.simulation_data['shortest_path']['columns'] = self.simulation_data['attributes']
        self.simulation_data['shortest_path'].column("#0", width=0, stretch=NO)
        self.simulation_data['shortest_path'].heading("#0", text='')
        for attribute in self.simulation_data['attributes']:
            self.simulation_data['shortest_path'].column(attribute, width=150)
            self.simulation_data['shortest_path'].heading(attribute, text=attribute)
        self.simulation_data['shortest_path'].pack(side=BOTTOM, anchor=S)

    def enter_map_data(self, event=None):
        errors = ''
        probabilities = self.data_entry['map_inputs_probabilities'].get().split(',')
        try:
            probabilities = [float(probability) for probability in probabilities]
            if sum(probabilities) != 1:
                errors += "Invalid probability: must sum to 1.\n"
            if len(probabilities) != 4:
                errors += "Invalid probabilities: maximum four entries, for each tile respectively.\n"
            else:
                self.map.weights = probabilities
        except ValueError:
            errors += "Invalid probability: numbers only.\n"

        try:
            width = int(self.data_entry['map_inputs_width'].get())
            if 5 <= width <= 50:
                self.map.map_width = width
                self.map_width = width
            else:
                errors += 'Map width: must be between 5 and 50\n'
        except ValueError:
            errors += "Map width: must be a number\n"

        try:
            height = int(self.data_entry['map_inputs_height'].get())
            if 5 <= height <= 15:
                self.map.map_height = height
                self.map_height = height
            else:
                errors += 'Map height: must be between 5 and 15\n'
        except ValueError:
            errors += "Map height: must be a number\n"
        if not errors:
            errors += "No errors."
            self.reset_simulation()
        else:
            errors = errors[0:-1]
        self.data_entry['error_string_var'].set(errors)

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
                elif self.map.map[column + row * self.map_width] == SPACE:
                    self.squares[column, row] = self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', tags='rect')
                elif self.map.map[column + row * self.map_width] == MOUNTAIN:
                    self.squares[column, row] = self.canvas.create_rectangle(x1, y1, x2, y2, fill='gray', tags='rect')
                self.cost[column, row] = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="-", fill='black',
                                                                 font='Helvetica 14 bold')

    def reset_simulation(self, event=None):
        self.canvas.delete('all')
        self.map.generate_map()
        self.squares = {}
        self.cost = {}
        self.algorithm_selected()
        self.simulation_data['shortest_path'].delete(*self.simulation_data['shortest_path'].get_children())
        self.configure_grid()
        self.buttons['button_simulation'].config(state=ACTIVE)

    def run_simulation(self, event=None):
        self.data_entry['algorithm_selection'].config(state=DISABLED)
        self.buttons['button_simulation'].config(state=DISABLED)
        self.buttons['button_reset_simulation'].config(state=DISABLED)
        self.buttons['map_inputs'].config(state=DISABLED)
        for cell in self.algorithm.traversal_path:
            column, row = cell.coordinate
            if self.map.map[column + row * self.map_width] == WATER:
                self.canvas.itemconfig(self.squares[column, row], fill='#21618C')
            elif self.map.map[column + row * self.map_width] == SPACE:
                self.canvas.itemconfig(self.squares[column, row], fill='#C04000')
            elif self.map.map[column + row * self.map_width] == MOUNTAIN:
                self.canvas.itemconfig(self.squares[column, row], fill='#566573')
            self.canvas.itemconfig(self.cost[column, row], fill='black', text=cell.f)
            self.canvas.update()
            time.sleep(self.simulation_speed)

        if self.algorithm.reached_goal:
            for cell in self.algorithm.shortest_path:
                self.simulation_data['shortest_path'].insert(parent='', iid=cell.coordinate, index=END,
                                                             values=(cell.coordinate, cell.f, cell.g, cell.h))
                column, row = cell.coordinate
                x1 = column * self.cell_width
                y1 = row * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height
                self.canvas.create_line(x1, y1, x2, y2)
                self.canvas.update()
                time.sleep(self.simulation_speed)
            self.simulation_data['shortest_path'].set(item=(0, 0), column='Reached Goal?',
                                                      value=str(self.algorithm.reached_goal))
        else:
            self.simulation_data['shortest_path'].insert(parent='', iid=0, index=END,
                                                         value=('-', '-', '-', '-', str(self.algorithm.reached_goal)))
        self.buttons['button_reset_simulation'].config(state=ACTIVE)
        self.data_entry['algorithm_selection'].config(state=NORMAL)
        self.buttons['map_inputs'].config(state=ACTIVE)

    def algorithm_selected(self, event=None):
        selected_indices = self.data_entry['algorithm_selection'].curselection()
        if selected_indices:
            algorithm = self.data_entry['algorithm_selection'].get(selected_indices)
            if algorithm == 'A*':
                self.algorithm = aStar.AStarSearch(self.map)
            elif algorithm == 'Breadth First Search':
                self.algorithm = bds.BDS(self.map)
            elif algorithm == 'Depth First Search':
                self.algorithm = dfs.DFS(self.map)
            elif algorithm == 'Dijkstra':
                self.algorithm = dijkstra.Dijkstra(self.map)

    def set_delay(self, value):
        self.simulation_speed = float(value) / 100
