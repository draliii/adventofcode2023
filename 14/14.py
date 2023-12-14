import copy
import hashlib


def read_data():
    pt1 = False
    f = open("14-full.in", "r")
    # f = open("14.in", "r")
    data = f.read().split("\n")
    data = list(map(list, data))

    return data


def solve(data):

    while True:
        moved = False
        for i in range(1, len(data)):
            for j in range(0, len(data[0])):
                if data[i][j] == "O":
                    if data[i-1][j] == ".":
                        # posun kamen nahoru
                        data[i-1] = data[i-1][:j] + "O" + data[i-1][j+1:]
                        data[i] = data[i][:j] + "." + data[i][j+1:]
                        moved = True
        if not moved:
            break

    weight_max = len(data)
    weights = 0
    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            if data[i][j] == "O":
                weights += weight_max - i

    return weights


def full_tilt(data, tiltx, tilty):
    fromi = 0
    toi = len(data)
    fromj = 0
    toj = len(data[0])

    if tiltx == -1:
        fromi = 1
    if tiltx == 1:
        toi = toi-1
    if tilty == -1:
        fromj = 1
    if tilty == 1:
        toj = toj-1

    while True:
        moved = False
        for i in range(fromi, toi):
            for j in range(fromj, toj):
                if data[i][j] == "O":
                    if data[i+tiltx][j+tilty] == ".":
                        # posun kamen nahoru
                        data[i+tiltx][j+tilty] = "O"
                        data[i][j] = "."
                        moved = True
        if not moved:
            break
    return


def full_tilt_N(data, stones):
    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            if data[i][j] == "O":
                target = stones[i][j]
                for t in range(target+1, i):
                    if data[t][j] == ".":
                        data[t][j] = "O"
                        data[i][j] = "."
                        break
    return
def full_tilt_S(data, stones):
    for i in range(len(data)-1, -1, -1):
        for j in range(0, len(data[0])):
            if data[i][j] == "O":
                target = stones[i][j]
                for t in range(target-1, i-1, -1):
                    if data[t][j] == ".":
                        data[t][j] = "O"
                        data[i][j] = "."
                        break
    return

def full_tilt_W(data, stones):
    # vse soupu doprava, prochazim zprava
    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            if data[i][j] == "O":
                target = stones[i][j]
                for t in range(target+1, j):
                    if data[i][t] == ".":
                        data[i][t] = "O"
                        data[i][j] = "."
                        break
    return

def full_tilt_E(data, stones):
    # vse soupu doprava, prochazim zprava
    for i in range(0, len(data)):
        for j in range(len(data[0])-1, -1, -1):
            if data[i][j] == "O":
                target = stones[i][j]
                for t in range(target-1, j-1, -1):
                    if data[i][t] == ".":
                        data[i][t] = "O"
                        data[i][j] = "."
                        break
    return


def new_array(rows, cols):
    array = []
    for i in range(rows):
        a = []
        for j in range(cols):
            a.append(0)
        array.append(a)
    return array


def get_min_stones(data):

    stonesN = new_array(len(data), len(data[0]))
    for cid in range(len(data[0])):
        last_stone = -1
        for rid in range(len(data)):
            if data[rid][cid] == "#":
                last_stone = rid
            stonesN[rid][cid] = last_stone

    stonesS = new_array(len(data), len(data[0]))
    for cid in range(len(data[0])):
        last_stone = len(data)
        for rid in range(len(data) - 1, -1, -1):
            if data[rid][cid] == "#":
                last_stone = rid
            stonesS[rid][cid] = last_stone

    stonesW = new_array(len(data), len(data[0]))
    for rid in range(len(data)):
        last_stone = -1
        for cid in range(len(data[0])):
            if data[rid][cid] == "#":
                last_stone = cid
            stonesW[rid][cid] = last_stone

    stonesE = new_array(len(data), len(data[0]))
    for rid in range(len(data)):
        last_stone = len(data[0])
        for cid in range(len(data[0])-1, -1, -1):
            if data[rid][cid] == "#":
                last_stone = cid
            stonesE[rid][cid] = last_stone

    return stonesN, stonesW, stonesS, stonesE



def print_arr(arr):
    for l in arr:
        print(l)
    print()

def str_arr(arr):
    r = ""
    for l in arr:
        r+=''.join(l)
    return r



def is_same(a1, a2):
    for i in range(len(a1)):
        for j in range(len(a1[0])):
            if a1[i][j] == a2[i][j]:
                continue
            else:
                return False
    return True


def solve_pt2(data, stonesN, stonesW, stonesS, stonesE):
    scores = []
    hashes = []
    looping = False

    for i in range(0, 1000000000):
        # data_before = copy.deepcopy(data)
        # print_arr(data)
        full_tilt_N(data, stonesN)
        # print_arr(data)
        full_tilt_W(data, stonesW)
        # print_arr(data)
        full_tilt_S(data, stonesS)
        # print_arr(data)
        full_tilt_E(data, stonesE)
        # print_arr(data)

        myhash = hashlib.md5(str_arr(data).encode('utf-8')).hexdigest()

        score = count_score(data)
        print(i, score, myhash)
        scores.append((i, score))

        if myhash in hashes:
            break
        else:
            hashes.append(myhash)

    first_hash = hashes.index(myhash)
    last_hash = len(hashes)
    loop_size = last_hash - first_hash

    offset = (1000000000 - first_hash) % loop_size
    idx = offset + first_hash -1
    print(scores[idx])
    k = 3


def count_score(data):
    weight_max = len(data)
    weights = 0
    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            if data[i][j] == "O":
                weights += weight_max - i

    return weights


if __name__ == '__main__':
    data = read_data()
    stonesN, stonesW, stonesS, stonesE = get_min_stones(data)
    print(solve_pt2(data, stonesN, stonesW, stonesS, stonesE))
