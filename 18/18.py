import math

import numpy as np
from PIL import Image


def read_data():
    pt1 = False
    # f = open("18-full.in", "r")
    f = open("18.in", "r")

    counters = {"R": 0, "L": 0, "U": 0, "D": 0}
    instructions = []
    data = f.read().split("\n")
    for d in data:
        (direction, distance, color) = d.split(" ")
        distance = int(distance)
        counters[direction] += distance
        instructions.append((direction, distance, color))

    return instructions, counters


def read_data_pt2():
    f = open("18-full.in", "r")
    # f = open("18.in", "r")

    counters = {"R": 0, "L": 0, "U": 0, "D": 0}
    directions = ["R", "D", "L", "U"]
    instructions = []
    data = f.read().split("\n")
    for d in data:
        (_, _, hexa) = d.split(" ")
        hexa = hexa.replace(")", "").replace("(", "")
        direction_code = int(hexa[6])
        direction = directions[direction_code]
        distance = int(hexa[1:6], 16)
        distance = int(distance)
        counters[direction] += distance
        instructions.append((direction, distance, 0))

    return instructions, counters


def flood_fill(data, start, value):
    # rucne, protoze se mi nechce instalovat scikit-image

    queue = [start]
    while True:
        if len(queue) == 0:
            return

        x, y = queue.pop(0)
        old_value = data[x, y]
        if old_value == value:
            continue

        data[x, y] = value

        for xdif, ydif in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            X = x + xdif
            Y = y + ydif
            if X < 0 or Y < 0 or X >= data.shape[0] or Y >= data.shape[1]:
                continue
            if data[X, Y] == old_value:
                queue.append((X, Y))


def solve(instructions, counters):
    row_count = counters["U"] + counters["D"]
    col_count = counters["L"] + counters["R"]
    offsets = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }

    field = np.zeros((col_count + 1, row_count + 1), dtype=np.uint8)

    x = counters["U"] - 1
    y = counters["L"] - 1
    for i, instruction in enumerate(instructions):
        direction, distance, color = instruction
        xdif, ydif = offsets[direction]
        xdif = xdif * (distance)
        ydif = ydif * (distance)
        newx = x + xdif
        newy = y + ydif

        a = min(x, newx)
        b = max(x, newx)
        c = min(y, newy)
        d = max(y, newy)

        field[a:b + 1, c:d + 1] = 255
        x += xdif
        y += ydif

        # im = Image.fromarray(np.uint8(field), "RGB")
        # im.save("foo" + str(i) + ".png")

    data = field[:, :]

    # flood the outside with 2s, replacing all zeros with 2
    flood_fill(data, (0, 0), 2)

    # replace all remaining 0s (on the inside) with ones
    data = np.where(data == 0, 255, data)

    # flood the outside with 0s, replacing all the outside with zeros
    flood_fill(data, (0, 0), 0)

    field[:, :, 0] = data
    im = Image.fromarray(np.uint8(field), "RGB")
    im.save("foo.png")

    print(np.sum(data) / 255)

    pass


def get_offsets(prev_direction, cur_direction, inside_right):
    corner = min(prev_direction, cur_direction) + max(prev_direction, cur_direction)
    if inside_right:
        if corner == "RU":
            return 0, 0
        elif corner == "DR":
            return 0, 1
        elif corner == "DL":
            return 1, 1
        elif corner == "LU":
            return 1, 0
        else:
            print(corner)
            raise ValueError
    else:
        raise ValueError


def parse_instructions_v2(instructions, counters):
    offsets = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }

    instructions.append(instructions[0])

    cornersx = {}
    downs = {}

    inside_right = True

    x, y = 0, 0
    prev_direction = "U"
    prev_corner = (0, 0)

    for i, instruction in enumerate(instructions):
        direction, distance, color = instruction

        xdif, ydif = offsets[direction]
        xdif = xdif * distance
        ydif = ydif * distance

        newx = x + xdif
        newy = y + ydif

        corner_offsets = get_offsets(prev_direction, direction, inside_right)
        corner_x = x + corner_offsets[0]
        corner_y = y + corner_offsets[1]

        append_in_dict(cornersx, corner_x, (corner_x, corner_y))
        if prev_direction == "U":
            downs[(corner_x, corner_y)] = prev_corner[0]
        elif prev_direction == "D":
            downs[prev_corner] = corner_x

        prev_corner = (corner_x, corner_y)
        prev_direction = direction
        x = newx
        y = newy

    min_corners_x = list(cornersx.keys())
    min_corners_x.sort()

    return cornersx, downs


def solve_pt2_v3(corners_x, downs):
    x_cuts = list(corners_x.keys())
    x_cuts.sort()
    result = 0

    for i in range(len(x_cuts)-1):
        x_cut = x_cuts[i]
        next_cut = x_cuts[i+1]

        # add new corners for ranges that go too low
        for corner in corners_x[x_cut]:
            if corner not in downs:
                continue
            if downs[corner] != next_cut:
                target_x = downs[corner]
                new_corner_x = next_cut
                new_corner_y = corner[1]
                new_corner = (new_corner_x, new_corner_y)
                downs[new_corner] = target_x
                append_in_dict(corners_x, new_corner_x, new_corner)

        width = 0
        corners_ys = []

        for corner in corners_x[x_cut]:
            if corner in downs:
                corners_ys.append(corner[1])

        corners_ys = list(set(corners_ys))
        corners_ys.sort()

        for i in range(0, len(corners_ys), 2):
            dif = corners_ys[i+1] - corners_ys[i]
            width += dif

        result += width * (next_cut-x_cut)
    return result


def append_in_dict(dictionary, index, data):
    if index not in dictionary.keys():
        dictionary[index] = []
    dictionary[index].append(data)


if __name__ == '__main__':
    instructions, counters = read_data_pt2()
    # print(solve(instructions, counters))
    print(solve_pt2_v3(*parse_instructions_v2(instructions, counters)))
