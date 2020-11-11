import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tkinter as tk
from tkinter import ttk
import calculate

class Board:
    def __init__(self, width, length, data):
        # Initialize the Board object
        self.length = length
        self.width = width
        self.velocity = [0 for i in range(width*length)]
        if data == 0:
            self.data = [0 for i in range(width*length)]
        else:
            self.data = data
        self.max = max(self.data)

    def get_position(self, x, y):
        # Returns the index of the coordinate in the list
        if x in range(0, self.width) and y in range(0, self.length):
            return x * self.length + y
        raise ValueError("Position out of range!")

    def get_adjacent(self, x, y):
        # Returns all adjacent values of the coordinate passed in
        all_adjacent = []
        if x >= 1:
            all_adjacent.append(self.get_position(x - 1, y))
        if y >= 1:
            all_adjacent.append(self.get_position(x, y - 1))
        if y <= self.length - 2:
            all_adjacent.append(self.get_position(x, y + 1))
        if x <= self.width - 2:
            all_adjacent.append(self.get_position(x + 1, y))
        return all_adjacent

    def display_board(self):
        # Simply display the board
        for i in range(0, self.length * self.width, self.length):
            print([int(self.data[i + x]) for x in range(self.length)])

    def apply_variations(self, val_map):
        # print([round(i,0) for i in self.velocity])
        # Apply the variations of heat to each heat parcel
        # print(sum([i for i in self.data]))

        for i in range(0, self.length):
            for j in range(0, self.width):
                self.data[self.get_position(i, j)] += val_map.data[val_map.get_position(i, j)]
                self.data[self.get_position(i, j)] += self.velocity[val_map.get_position(i, j)]
        self.velocity += val_map.data
    
    def add_heat_source(self, x, y, amount):
        self.data[(self.get_position(x,y))] = amount 
        self.max = amount

# Calculates the amount of heat each parcel adjacent to the input parcel gets
# Input:
# x, y: coords of the parcel to calculate
# board: calculate changes from the board


def calculate_val(x, y, board):
    # distribute_to: adjacent parcels to the parcel in question that receive heat
    distribute_to = board.get_adjacent(x, y)
    heat_quantity = board.data[board.get_position(x, y)]

    '''
    Heat transfer formula: Q/t =  kA(T2 - T1)/d
    Where:
    Q = the energy lost/gained,
    t = the variation in time,
    k = thermic distribution constant of air, approx 1.4 of air,
    A = surface area in contact,
    T2 = temperature of the first object,
    T1 = temperature of the second object,
    d = thickness of the wall separating both, 0.01 everytime (approx).

    Determine which adjacents must be ignored.
    Volumetric heat capacity of air: 1.256 kJ m^−3 K^-1,
    Temperature of a parcel of air: T = Q * 1.256 * 0.1^-3
    '''
    scale = 200

    k = 1.4
    A = 0.1**2
    d = 0.01
    T1 = heat_quantity * 1.256 * (0.1**3)
    heat_var = 0
    for i in distribute_to:
        heat_adj = board.data[i]
        T2 = heat_adj * 1.256 * (0.1**3)
        heat_var -= k * A * (T2 - T1) / (d * 2)
    return heat_var * scale

# Input: coordinate map
# Output: value map (changes)
# Determine the instantaneous rate of change of heat of the system

def det_distrib(board):
    val_map = Board(board.length, board.width, 0)
    for i in range(0, val_map.width):
        for j in range(0, val_map.length):
            # new_vals: list of modified adjacents
            # 2D list: List of vector. val[0]: x, val[1]: y, val[2]: value to add
            new_val = calculate_val(i, j, board)
            val_map.data[val_map.get_position(i, j)] = -new_val
    return val_map

def animate_2d_heat_map(board):
    fig = plt.figure()

    data = np.reshape(board.data, (-1, board.length))

    ax = sns.heatmap(data, vmin=0, vmax=board.max, cmap="jet")

    def init():
        plt.clf()
        ax = sns.heatmap(data, vmin=0, vmax=board.max, cmap="jet")

    def animate(i):
        plt.clf()
        val_map = det_distrib(board)
        board.apply_variations(val_map)
        # board.add_heat_source(0,0,10)
        # board.add_heat_source(0,9,10)
        # board.add_heat_source(9,0,10)
        # board.add_heat_source(9,9,10)
        data = np.reshape(board.data, (-1, board.length))
        ax = sns.heatmap(data, vmin=0, vmax=board.max, cmap="jet")

    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=250)
    plt.show()

def animate_3d_heat_map(board):
    fig = plt.figure()

    ax = fig.gca(projection='3d')

    X = [i for i in range(0, board.width)]
    Y = [j for j in range(0, board.length)]
    X, Y = np.meshgrid(X, Y)
    Z = np.asarray(np.reshape(board.data, (-1, board.width)))
    mappable = plt.cm.ScalarMappable(cmap = "jet")
    mappable.set_array(Z)
    mappable.set_clim(0, board.max)

    surf = ax.plot_surface(X, Y, Z, cmap=mappable.cmap, norm=mappable.norm, linewidth=0, antialiased=True)

    fig.colorbar(surf)
    def init():
        ax.clear()
        surf = ax.plot_surface(X, Y, Z, cmap=mappable.cmap, norm=mappable.norm, linewidth=0, antialiased=True)

    def animate(i):
        ax.clear()
        val_map = det_distrib(board)
        board.apply_variations(val_map)
        # board.add_heat_source(0,0,10)
        # board.add_heat_source(0,9,10)
        # board.add_heat_source(9,0,10)
        # board.add_heat_source(9,9,10)3
        Z = np.asarray(np.reshape(board.data, (-1, board.width)))
        surf = ax.plot_surface(X, Y, Z,  cmap=mappable.cmap, norm=mappable.norm, linewidth=0, antialiased=True)
        ax.set_zlim(0, board.max)

    plot = [ax.plot_surface(X, Y, Z, color='0.75')]

    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=1000)

    plt.show()

def main():
    # root = tk.Tk()
    # root.title("Task-Failed-Successfully!") 
    # length = ttk.Label(root, text = "Enter the length:").grid(column = 0, row = 0)
    # width = ttk.Label(root, text = "Enter the width:").grid(column = 0, row = 2)  
    # def click():   
    #     root.destroy()
    # length_val = tk.StringVar()  
    # width_val = tk.StringVar()
    # length_entered = ttk.Entry(root, width = 12, textvariable = length_val).grid(column = 0, row = 1)
    # width_entered = ttk.Entry(root, width = 12, textvariable = width_val).grid(column = 0, row = 3)
    # button = ttk.Button(root, text = "submit", command = click).grid(column = 0, row = 5)  
    # root.mainloop()

    # # Board parameters
    # board_length = int(length_val.get())
    # board_width = int(width_val.get())

    board_length_2d = 169
    board_width_2d = 169
    board_data_2d = calculate.get_data('data.csv')
    # board_data_2d[0] = 10

    board_length_3d = 169
    board_width_3d = 169
    board_data_3d = calculate.get_data('data.csv')
    # board_data_3d = [0 for x in range(board_length_3d) for y in range(board_width_3d)]

    # board_data_3d[0] = 10
    # board_data_3d[99] = 10
    # board_data_3d[24] = 10
    # board_data_3d[74] = 10

    primary_board = Board(board_length_2d, board_width_2d, board_data_2d)
    second_board = Board(board_length_3d, board_width_3d, board_data_3d)

    animate_2d_heat_map(primary_board)
    animate_3d_heat_map(second_board)

if __name__ == "__main__":
    main()
