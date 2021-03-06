import statistics
import pandas

def get_data(file_name, clean_up=False, divide=0):

    def get_position(x, y, side_length):
        # Returns the index of the coordinate in the list
        if x in range(0, side_length) and y in range(0, side_length):
            return x * side_length + y
        # print(x, y, side_length)
        raise ValueError("Position out of range!")

    def get_coordinate(pos, side_length):
        # Returns the coordinate of the index in the list
        if pos < side_length**2:
            return (int(pos/side_length), pos % side_length)
        # print(pos, side_length)
        raise ValueError("Position out of range!")

    def get_adjacent(x, y, side_length):
        # Returns all adjacent values of the coordinate passed in
        all_adjacent = []
        if x >= 1:
            all_adjacent.append(get_position(x - 1, y, side_length))
        if y >= 1:
            all_adjacent.append(get_position(x, y - 1, side_length))
        if y <= side_length - 2:
            all_adjacent.append(get_position(x, y + 1, side_length))
        if x <= side_length - 2:
            all_adjacent.append(get_position(x + 1, y, side_length))
        return all_adjacent

    df = pandas.read_csv(file_name)

    df.sort_values(by=['x', 'y'])

    # [WIP] Hard code this value for now
    side_length = 169

    # Generate a empty list filled with zero based on the side length
    output = [0 for x in range(side_length) for y in range(side_length)]

    # Assign the temp values we collected to the output list
    for index, row in df.iterrows():
        output[get_position(int(row['x']), int(row['y']), side_length)] = int(df.iloc[index]['temp'])

    # clean_up will fix up the area with 0 temperature
    if clean_up:
        checks = [(x, y) for x in range(0, side_length, divide) for y in range(0, side_length, divide)]
        output_fixed = []
        # Go through all the temp values and append them to a list with reduced size
        for coor in checks:
            values = []
            for x in range(coor[0], coor[0] + divide):
                for y in range(coor[1], coor[1] + divide):
                    values.append(output[get_position(x, y, side_length)])
            output_fixed.append(max(values))
        # Keep looing until there is no more 0 value
        while 0 in output_fixed:
            for i in range(len(output_fixed)):
                if output_fixed[i] == 0:
                    x, y = get_coordinate(i, int(side_length**(1/2)))
                    adjacent = get_adjacent(x, y, int(side_length**(1/2)))
                    values = [output_fixed[i] for i in adjacent if output_fixed[i] != 0]
                    if values != []:
                        output_fixed[i] = statistics.mean(values)
        return output_fixed
    return output

# get_data('data.csv', True, 13)
