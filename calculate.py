import pandas

def get_data(file_name, clean_up=False, divide=0):

    def get_position(x, y, side_length):
        # Returns the index of the coordinate in the list
        if x in range(0, side_length) and y in range(0, side_length):
            return x * side_length + y
        raise ValueError("Position out of range!")

    df = pandas.read_csv(file_name)

    df.sort_values(by=['x', 'y'])

    # [WIP] Hard code this value for now
    side_length = 169

    output = [0 for x in range(side_length) for y in range(side_length)]

    for index, row in df.iterrows():
        output[get_position(int(row['x']), int(row['y']), side_length)] = int(df.iloc[index]['temp'])

    if clean_up:
        checks = [(x, y) for x in range(0, side_length, divide) for y in range(0, side_length, divide)]
        output_fixed = []
        for coor in checks:
            values = []
            for x in range(coor[0], coor[0] + divide):
                for y in range(coor[1], coor[1] + divide):
                    values.append(output[get_position(x, y, side_length)])
            output_fixed.append(max(values))
        return output_fixed
    else:
        return output

# get_data('data.csv', True, 13)
