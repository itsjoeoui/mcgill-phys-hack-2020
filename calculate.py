import pandas
def get_data():
    def get_position(x, y, size):
        # Returns the index of the coordinate in the list
        if x in range(0, size) and y in range(0, size):
            return x * size + y
        raise ValueError("Position out of range!")

    def get_adjacent(data, x, y, size):
        # Returns all adjacent values of the coordinate passed in
        all_adjacent = []
        if x >= 1:
            all_adjacent.append(get_position(x - 1, y, size))
        if y >= 1:
            all_adjacent.append(get_position(x, y - 1, size))
        if y <= size - 2:
            all_adjacent.append(get_position(x, y + 1, size))
        if x <= size - 2:
            all_adjacent.append(get_position(x + 1, y, size))
        return all_adjacent

    def display_board(data, size):
        # Simply display the board
        for i in range(0, size**2, size):
            print([int(data[i + x]) for x in range(size)])

    df = pandas.read_csv('data.csv')

    df.sort_values(by=['x', 'y'])

    size = int((len(df.index)))
    output = [0 for x in range(size) for y in range(size)]

    for index, row in df.iterrows():
        output[get_position(int(row['x']), int(row['y']), size)] = int(df.iloc[index]['temp'])

    return output