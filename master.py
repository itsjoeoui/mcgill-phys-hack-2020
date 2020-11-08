import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class Board:
    def __init__(self, width, length, data):
        # Initialize the Board object
        self.length = length
        self.width = width
        self.data = []
        self.velocity = []
        for i in range(width*length):
                self.velocity.append(0)
        if data == 0:
            for i in range(width*length):
                self.data.append(0)
        else:
            self.data = data

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
        print(sum([i for i in self.data]))

        for i in range(0, self.length):
            for j in range(0, self.width):
                self.data[self.get_position(i, j)] += val_map.data[val_map.get_position(i, j)]
                self.data[self.get_position(i, j)] += self.velocity[val_map.get_position(i, j)]
        self.velocity += val_map.data
    
    def add_heat_source(self, x, y, amount):
        self.data[(self.get_position(x,y))] = amount 

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
    scale = 300

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


def animate_heat_map(board):
    fig = plt.figure()

    data = np.reshape(board.data, (-1, board.length))
    ax = sns.heatmap(data, vmin=0, vmax=10, cmap="jet")

    def init():
        plt.clf()
        ax = sns.heatmap(data, vmin=0, vmax=10, cmap="jet")

    def animate(i):
        plt.clf()
        val_map = det_distrib(board)
        board.apply_variations(val_map)
        # board.add_heat_source(0,0,10)
        # board.add_heat_source(0,9,10)
        # board.add_heat_source(9,0,10)
        # board.add_heat_source(9,9,10)
        data = np.reshape(board.data, (-1, board.length))
        ax = sns.heatmap(data, vmin=0, vmax=10, cmap="jet")

    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=1000)

    plt.show()

def main():
    board_length = 10
    board_width = 10
    board_data = [0 for x in range(board_length) for y in range(board_width)]
    board_data[0] = 10

    # print(board_data)

    main_board = Board(board_length, board_width, board_data)

    animate_heat_map(main_board)

if __name__ == "__main__":
    main()
