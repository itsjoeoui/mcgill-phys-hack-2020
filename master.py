import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import calculate

class Board:
    def __init__(self, data, size):
        # Initialize the Board object
        self.size = size
        if data == 0:
            self.data = [0 for i in range(size**2)]
        else:
            self.data = data
        self.velocity = [0 for i in range(len(self.data))]
        self.max = max(self.data)

    def get_position(self, x, y):
        # Returns the index of the coordinate in the list
        if x in range(0, self.size) and y in range(0, self.size):
            return x * self.size + y
        raise ValueError("Position out of range!")

    def get_adjacent(self, x, y):
        # Returns all adjacent values of the coordinate passed in
        all_adjacent = []
        if x >= 1:
            all_adjacent.append(self.get_position(x - 1, y))
        if y >= 1:
            all_adjacent.append(self.get_position(x, y - 1))
        if y <= self.size - 2:
            all_adjacent.append(self.get_position(x, y + 1))
        if x <= self.size - 2:
            all_adjacent.append(self.get_position(x + 1, y))
        return all_adjacent

    def display_board(self):
        # Simply display the board
        for i in range(0, len(data), self.size):
            print([int(self.data[i + x]) for x in range(self.size)])

    def apply_variations(self, val_map):
        # print([round(i,0) for i in self.velocity])
        # Apply the variations of heat to each heat parcel
        # print(sum([i for i in self.data]))

        for i in range(0, self.size):
            for j in range(0, self.size):
                self.data[self.get_position(i, j)] += val_map.data[val_map.get_position(i, j)]
                self.data[self.get_position(i, j)] += self.velocity[val_map.get_position(i, j)]
        self.velocity += val_map.data

    def add_heat_source(self, x, y, amount):
        self.data[(self.get_position(x, y))] = amount
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
    val_map = Board(0, board.size)
    for i in range(0, val_map.size):
        for j in range(0, val_map.size):
            # new_vals: list of modified adjacents
            # 2D list: List of vector. val[0]: x, val[1]: y, val[2]: value to add
            new_val = calculate_val(i, j, board)
            val_map.data[val_map.get_position(i, j)] = -new_val
    return val_map

def animate_2d_heat_map(board, anim=True):
    fig = plt.figure()

    data = np.reshape(board.data, (-1, board.size))

    ax = sns.heatmap(data, vmin=0, vmax=board.max, cmap="jet")

    if anim:
        def init():
            plt.clf()
            ax = sns.heatmap(data, vmin=0, vmax=board.max, cmap="jet")

        def animate(i):
            plt.clf()
            val_map = det_distrib(board)
            board.apply_variations(val_map)
            data = np.reshape(board.data, (-1, board.size))
            ax = sns.heatmap(data, vmin=0, vmax=board.max, cmap="jet")

        anim = animation.FuncAnimation(fig, animate, init_func=init, interval=250)
    else:
        plt.clf()
        ax = sns.heatmap(data, vmin=0, vmax=board.max, cmap="jet")

    plt.show()

def animate_3d_heat_map(board, anim=True):
    fig = plt.figure()

    ax = fig.gca(projection='3d')

    X = [i for i in range(0, board.size)]
    Y = [j for j in range(0, board.size)]
    X, Y = np.meshgrid(X, Y)
    Z = np.asarray(np.reshape(board.data, (-1, board.size)))

    mappable = plt.cm.ScalarMappable(cmap="jet")
    mappable.set_array(Z)
    mappable.set_clim(0, board.max)

    surf = ax.plot_surface(X, Y, Z, cmap=mappable.cmap, norm=mappable.norm, linewidth=0, antialiased=True)

    fig.colorbar(surf)

    if anim:
        def init():
            ax.clear()
            surf = ax.plot_surface(X, Y, Z, cmap=mappable.cmap, norm=mappable.norm, linewidth=0, antialiased=True)

        def animate(i):
            ax.clear()
            val_map = det_distrib(board)
            board.apply_variations(val_map)
            Z = np.asarray(np.reshape(board.data, (-1, board.size)))
            surf = ax.plot_surface(X, Y, Z, cmap=mappable.cmap, norm=mappable.norm, linewidth=0, antialiased=True)
            ax.set_zlim(0, board.max)

        plot = [ax.plot_surface(X, Y, Z, color='0.75')]

        anim = animation.FuncAnimation(fig, animate, init_func=init, interval=1000)
    else:
        ax.clear()
        surf = ax.plot_surface(X, Y, Z, cmap=mappable.cmap, norm=mappable.norm, linewidth=0, antialiased=True)

    plt.show()

def main():
    board_data_2d = calculate.get_data('data1.csv')
    board_size_2d = int(math.sqrt(len(board_data_2d)))
    board_2d = Board(board_data_2d, board_size_2d)
    animate_2d_heat_map(board_2d, False)

    board_data_2d_fixed = calculate.get_data('data1.csv', True, 13)
    board_size_2d_fixed = int(math.sqrt(len(board_data_2d_fixed)))
    board_2d_fixed = Board(board_data_2d_fixed, board_size_2d_fixed)
    animate_2d_heat_map(board_2d_fixed)

    board_data_3d = calculate.get_data('data1.csv')
    board_size_3d = int(math.sqrt(len(board_data_3d)))
    board_3d = Board(board_data_3d, board_size_3d)
    animate_3d_heat_map(board_3d, False)

    board_data_3d_fixed = calculate.get_data('data1.csv', True, 13)
    board_size_3d_fixed = int(math.sqrt(len(board_data_3d_fixed)))
    board_3d_fixed = Board(board_data_3d_fixed, board_size_3d_fixed)
    animate_3d_heat_map(board_3d_fixed)

if __name__ == "__main__":
    main()
