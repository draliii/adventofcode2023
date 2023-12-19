import math

import numpy as np
from PIL import Image


def read_data():
    pt1 = False
    f = open("18-full.in", "r")
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

    field = np.zeros((col_count+1, row_count+1), dtype=np.uint8)

    x = counters["U"]-1
    y = counters["L"]-1
    for i, instruction in enumerate(instructions):
        direction, distance, color = instruction
        xdif, ydif = offsets[direction]
        xdif = xdif * (distance)
        ydif = ydif * (distance)
        newx = x + xdif
        newy = y + ydif

        a = min(x,newx)
        b = max(x,newx)
        c = min(y,newy)
        d = max(y,newy)

        field[a:b+1, c:d+1] = 255
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

    print(np.sum(data)/255)

    pass


def solve_pt2(instructions, counters):

    offsets = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }

    cornersx = {}
    cornersy = {}

    x, y = 0, 0
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
        append_in_dict(cornersx, a, (a, c, b, d, distance))

        x = newx
        y = newy

    min_corners_x = list(cornersx.keys())
    min_corners_x.sort()
    score = 0

    for i in range(len(min_corners_x)-1):
        corner_x = min_corners_x[i]
        neighbors = cornersx[corner_x]

        this_round_width = 0
        this_round_height = min_corners_x[i+1] - min_corners_x[i+1]
        for n in neighbors:
            x, y, newx, newy, distance = n

            if newx < corner_x:
                continue

            if x == corner_x:
                if x == newx:  # tohle je posun do strany, ne nahoru/dolu
                    this_round_width += distance + 1

                else:  # je to posun nahoru/dolu
                    if x <= corner_x + this_round_height:  # je to trasa nade mnou, kterou uz muzu zahodit
                        cornersx[min_corners_x[i+1]].remove(n)
                    else:
                        append_in_dict(cornersx, newx, (newx))


        for n in neighbors:
            x, y, newx, newy, distance = n

        if this_round_height == corner_x + this_round_height:
            pass
        k = 3

        print(this_round_width)
        score += this_round_height * this_round_width



    pass


def parse_instructions(instructions, counters):
    offsets = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }

    cornersx = {}
    cornersy = {}

    x, y = 0, 0
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
        append_in_dict(cornersx, a, (a, c, b, d, distance))

        x = newx
        y = newy

    min_corners_x = list(cornersx.keys())
    min_corners_x.sort()

    corners_x_down = {
        0: [(0, 2), (7, 5)],
        2: [(2, 5)],
        5: [(0, 7), (4, 7)],
        7: [(1, 9), (7, 9)]
    }
    # klic je x
    # v poli jsou pak dvojice (y, cilove x)

    corners_x_right = {
        0: [(0, 6)],
        2: [(0, 2)],
        5: [(0, 2), (4, 6)],
        7: [(0, 1), (4, 6)],
        9: [(1, 6)]
    }
    # klic je x
    # v poli jsou dvojice (y, cilove y)

    return min_corners_x, corners_x_down, corners_x_right


def solve_pt2_v2(minxs, corners_x_down, corners_x_right):
    x_cuts = [0, 3, 5, 6, 7, 8, 10]
    y_cuts_in_interval = {
        0: [0, 7],
        3: [2, 7],
        5: [0, 7],
        6: [0, 3, 3, 5],
        7: [0, 7],
        8: [1, 7]
    }

    x_cuts = [0]
    y_cuts_in_interval = {}

    for x in list(corners_x_right.keys())[1:]:
        x_cuts.append(x)
        x_cuts.append(x+1)


    # klic je x
    # v poli jsou pak dvojice (y, cilove x)
    corners_x_down = {
        0: [(0, 2), (6, 5)],
        2: [(2, 5), (6, 5)],
        5: [(0, 7), (4, 7)],
        7: [(1, 9), (6, 9)]
    }

    for i in range(len(x_cuts)):
        x_cut = x_cuts[i]

        if x_cut not in corners_x_down.keys():
            y_cuts = y_cuts_in_interval[x_cuts[i-1]]
            append_in_dict(y_cuts_in_interval, x_cuts[i], y_cuts)
            continue

        downs = list(map(lambda a: a[0], corners_x_down[x_cut]))
        for cxr in corners_x_right[x_cut]:
            downs.append(cxr[0])
            downs.append(cxr[1])
        downs = remove_pairs(downs)


        from_ys = downs[::2]
        to_ys = downs[1::2]
        for from_y, to_y in zip(from_ys, to_ys):
            append_in_dict(y_cuts_in_interval, x_cuts[i], from_y)
            append_in_dict(y_cuts_in_interval, x_cuts[i], to_y+1)
        pass

    print(x_cuts)



    result = 0
    for xi in range(len(x_cuts)-1):
        x = x_cuts[xi]
        height = x_cuts[xi+1] - x
        width = 0

        from_ys = y_cuts_in_interval[x][::2]
        to_ys = y_cuts_in_interval[x][1::2]
        for from_y, to_y in zip(from_ys, to_ys):
            width += to_y - from_y

        result += height*width
    return result


def append_in_dict(dictionary, index, data):
    if index not in dictionary.keys():
        dictionary[index] = []
    dictionary[index].append(data)


if __name__ == '__main__':
    instructions, counters = read_data_pt2()
    print(solve(instructions, counters))
    # print(solve_pt2_v2(*parse_instructions(instructions, counters)))
