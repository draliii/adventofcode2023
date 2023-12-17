from queue import PriorityQueue


def read_data():
    pt1 = False
    f = open("17-full.in", "r")
    # f = open("17.in", "r")
    # f = open("17-v2.in", "r")
    data = f.read().split("\n")
    data = list(map(lambda d: list(map(int, list(d))), data))
    return data


def new_array(rows, cols, initval=0):
    array = []
    for i in range(rows):
        a = [initval] * cols
        array.append(a)
    return array


def get_new_direction(fromx, fromy, xdif, ydif):
    # pokud se obraci smer o 180, tak to muzu rovnou zahodit
    if fromx > 0 and xdif < 0:
        return False, 0, 0
    if fromx < 0 and xdif > 0:
        return False, 0, 0
    if fromy > 0 and ydif < 0:
        return False, 0, 0
    if fromy < 0 and ydif > 0:
        return False, 0, 0

    newfromx = fromx + xdif
    newfromy = fromy + ydif
    # pokud se meni smer o 90, tak vracim nove smery
    if min(abs(newfromx), abs(newfromy)) > 0:
        return True, xdif, ydif

    # pokud prelezu 3, tak je to spatne
    if abs(newfromx) > 3 or abs(newfromy) > 3:
        return False, 0, 0

    return True, newfromx, newfromy

    pass


def s(option):
    return str(option[0]) + str(option[1])



def solve_v2(data):
    max_val = sum([sum(d) for d in data])

    options = [(0, 0), (-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3, 0), (0, -3), (0, -2), (0, -1), (0, 1), (0, 2), (0, 3)]
    options_s = list(map(s, options))

    best_values = {}
    for o in options_s:
        best_values[o] = new_array(len(data), len(data[0]), initval=max_val)
        best_values[o][0][0] = 0

    queue = PriorityQueue()
    # value, x, y, fromx, fromy
    queue.put((0, 0, 0, 0, 0))

    while True:
        if queue.empty():
            break

        value, x, y, fromx, fromy = queue.get()

        if x == len(data) -1 and y == len(data[0]) -1:
            break

        for xdif, ydif in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            newx = x + xdif
            newy = y + ydif

            # todo make sure there is no straight line
            success, newfromx, newfromy = get_new_direction(fromx, fromy, xdif, ydif)
            if not success:
                continue

            # do not leave the array
            if newx >= len(data) or newx < 0 or newy >= len(data[0]) or newy < 0:
                continue

            prev_val = best_values[s((newfromx, newfromy))][newx][newy]
            loss = data[newx][newy]
            new_val = value + loss

            if new_val < prev_val:
                best_values[s((newfromx, newfromy))][newx][newy] = new_val
                queue.put((new_val, newx, newy, newfromx, newfromy))

    min_value = max_val
    for o in options_s:
        if best_values[o][len(data)-1][len(data[0])-1] < min_value:
            min_value = best_values[o][len(data)-1][len(data[0])-1]
    print(min_value)

    pass


def get_new_direction_pt2(fromx, fromy, xdif, ydif):
    # pokud se obraci smer o 180, tak to muzu rovnou zahodit
    if fromx > 0 and xdif < 0:
        return False, 0, 0
    if fromx < 0 and xdif > 0:
        return False, 0, 0
    if fromy > 0 and ydif < 0:
        return False, 0, 0
    if fromy < 0 and ydif > 0:
        return False, 0, 0

    newfromx = fromx + xdif
    newfromy = fromy + ydif

    # pokud se meni smer o 90, musim mit aspon 4
    if min(abs(newfromx), abs(newfromy)) > 0:
        if abs(fromx) > 3 or abs(fromy) > 3:
            return True, xdif, ydif
        else:
            return False, 0, 0

    # pokud prelezu 3, tak je to spatne
    if abs(newfromx) > 10 or abs(newfromy) > 10:
        return False, 0, 0

    return True, newfromx, newfromy


def solve_pt2(data):
    max_val = sum([sum(d) for d in data])

    options = [(0, 0), (0, 1), (1, 0), (-1, 0), (0, -1), (0, 2), (2, 0), (-2, 0), (0, -2),
               (0, 3), (3, 0), (-3, 0), (0, -3), (0, 4), (4, 0), (-4, 0), (0, -4), (0, 5), (5, 0), (-5, 0), (0, -5),
               (0, 6), (6, 0), (-6, 0), (0, -6), (0, 7), (7, 0), (-7, 0), (0, -7), (0, 8), (8, 0), (-8, 0), (0, -8),
               (0, 9), (9, 0), (-9, 0), (0, -9), (0, 10), (10, 0), (-10, 0), (0, -10)]

    end_options = [(0, 4), (4, 0), (-4, 0), (0, -4), (0, 5), (5, 0), (-5, 0), (0, -5),
               (0, 6), (6, 0), (-6, 0), (0, -6), (0, 7), (7, 0), (-7, 0), (0, -7), (0, 8), (8, 0), (-8, 0), (0, -8),
               (0, 9), (9, 0), (-9, 0), (0, -9), (0, 10), (10, 0), (-10, 0), (0, -10)]

    options_s = list(map(s, options))
    end_options_s = list(map(s, end_options))

    best_values = {}
    for o in options_s:
        best_values[o] = new_array(len(data), len(data[0]), initval=max_val)
        best_values[o][0][0] = 0

    queue = PriorityQueue()
    # value, x, y, fromx, fromy
    queue.put((0, 0, 0, 0, 0))

    while True:
        if queue.empty():
            break

        value, x, y, fromx, fromy = queue.get()

        for xdif, ydif in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            newx = x + xdif
            newy = y + ydif

            success, newfromx, newfromy = get_new_direction_pt2(fromx, fromy, xdif, ydif)
            if not success:
                continue

            # do not leave the array
            if newx >= len(data) or newx < 0 or newy >= len(data[0]) or newy < 0:
                continue

            prev_val = best_values[s((newfromx, newfromy))][newx][newy]
            loss = data[newx][newy]
            new_val = value + loss

            if new_val < prev_val:
                best_values[s((newfromx, newfromy))][newx][newy] = new_val
                queue.put((new_val, newx, newy, newfromx, newfromy))

    min_value = max_val
    for o in end_options_s:
        # print(o, best_values[o][len(data)-1][len(data[0])-1])
        if best_values[o][len(data)-1][len(data[0])-1] < min_value:
            min_value = best_values[o][len(data)-1][len(data[0])-1]
    print(min_value)

    pass

if __name__ == '__main__':
    data = read_data()
    print(solve_pt2(data))
