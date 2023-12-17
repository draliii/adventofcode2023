def read_data():
    pt1 = False
    f = open("22-full.in", "r")
    f = open("22.in", "r")
    data = f.read().split("\n")
    return data


def solve(data):
    pass


if __name__ == '__main__':
    data = read_data()
    print(solve(data))
