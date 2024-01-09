def read_data():
    pt1 = False
    f = open("20-full.in", "r")
    # f = open("20.in", "r")
    data = f.read().split("\n")
    return data


def solve(data):
    pass


if __name__ == '__main__':
    data = read_data()
    print(solve(data))
