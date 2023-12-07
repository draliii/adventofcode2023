import math


def read_input():
    f = open("6-full.in", "r")
    lines = f.read().split("\n")

    times = list(map(int, ' '.join(lines[0].split(":")[1].split()).split(" ")))
    distances = list(map(int, ' '.join(lines[1].split(":")[1].split()).split(" ")))
    return times, distances


def read_input_pt2():
    f = open("6-full.in", "r")
    lines = f.read().split("\n")

    times = [int(lines[0].split(":")[1].replace(" ", ""))]
    distances = [int(lines[1].split(":")[1].replace(" ", ""))]
    return times, distances


def get_interval(t, d):
    D = math.sqrt(t*t - 4*d)
    start = math.floor(((t-D)/2) +1)
    end = math.ceil(((t+D)/2)-1)
    return end-start+1


if __name__ == '__main__':
    times, distances = read_input_pt2()
    result = 1
    for t, d in zip(times, distances):
        result = result*get_interval(t, d)
    print(result)
