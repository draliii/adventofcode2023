def read_data():
    pt1 = False
    f = open("13-full.in", "r")
    # f = open("13.in", "r")
    data = f.read().split("\n")

    mirrors = []
    mirror = []
    for d in data:
        if d == "":
            mirrors.append(mirror)
            mirror = []
        else:
            mirror.append(d)

    return mirrors


def solve(mirrors):
    pass


if __name__ == '__main__':
    mirrors = read_data()
    print(solve(mirrors))
