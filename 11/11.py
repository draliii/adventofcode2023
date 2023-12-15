import numpy as np

def read_data():
    f = open("11-full.in", "r")
    # f = open("11.in", "r")
    data = f.read().split("\n")

    skipi = []
    skipj = []
    stars = []

    I = 0
    for i in range(0, len(data)):
        canskipi = True
        for j in range(0, len(data[0])):
            if data[i][j] == "#":
                stars.append((i, j))
                canskipi = False
        if canskipi:
            I += 1
        skipi.append(I)

    J = 0
    for j in range(0, len(data[0])):
        canskipj = True
        for i in range(0, len(data)):
            if data[i][j] == "#":
                canskipj = False
        if canskipj:
            J += 1
        skipj.append(J)

    return stars, skipi, skipj


def new_array(rows, cols):
    array = []
    for i in range(rows):
        a = [0] * cols
        array.append(a)
    return array


def get_distance(first, second, skipi, skipj, coef=1):
    a = abs(first[0] - second[0])
    b = abs(first[1] - second[1])

    iskips = abs(skipi[first[0]]-skipi[second[0]])
    jskips = abs(skipj[first[1]]-skipj[second[1]])

    return a+b + jskips*coef + iskips*coef
    pass


def solve(stars, skipi, skipj):
    d = 0
    for f in range(len(stars)):
        for s in range(f+1, len(stars)):
            first = stars[f]
            second = stars[s]
            distance = get_distance(first, second, skipi, skipj, coef=999999)
            print(f+1, s+1, distance)
            d += distance
    print(d)

    pass


if __name__ == '__main__':
    stars, skipi, skipj = read_data()
    solve(stars, skipi, skipj)
