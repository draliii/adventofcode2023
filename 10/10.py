from math import lcm

def read_data():
    f = open("10-full.in", "r")
    f = open("10.in", "r")
    data = f.read().split("\n")

    result = []
    for d in data:
        result.append(list(map(int, d.split(" "))))

    return result


def solve(data):
    pass


if __name__ == '__main__':
    data = read_data()
    solve(data)
