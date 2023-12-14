def read_data():
    pt1 = False
    f = open("13-full.in", "r")
    #f = open("13.in", "r")
    data = f.read().split("\n")

    mirrors = []
    mirror = []
    for d in data:
        if d == "":
            row_sums = list(map(lambda row: int(row.replace(".", "0").replace("#", "1"), 2), mirror))
            transposed = list(map(lambda l: ''.join(l), map(list, zip(*mirror))))
            col_sums = list(map(lambda row: int(row.replace(".", "0").replace("#", "1"), 2), transposed))
            mirrors.append((mirror, row_sums, col_sums))
            mirror = []
        else:
            mirror.append(d)

    return mirrors


def check_reflection(sums, idx):
    after = sums[idx:]
    before = sums[:idx]
    before = before[::-1]
    # print(list(zip(before, after)))
    for a, b in list(zip(after, before)):
        if a != b:
            return False
    return True


def solve_mirror(m):
    mirror, rows, cols = m
    for ri in range(len(rows) - 1):
        if rows[ri] == rows[ri + 1]:
            if check_reflection(rows, ri + 1):
                return 100*(ri+1)
    for ci in range(len(cols) - 1):
        if cols[ci] == cols[ci + 1]:
            if check_reflection(cols, ci + 1):
                return ci+1


def solve(mirrors):
    summ = 0
    for m in mirrors:
        s = solve_mirror(m)
        summ += s
    print(summ)


if __name__ == '__main__':
    mirrors = read_data()
    solve(mirrors)
