from math import lcm

def read_data():
    f = open("9-full.in", "r")
    # f = open("9.in", "r")
    # f = open("9-pt2.in", "r")
    data = f.read().split("\n")

    result = []
    for d in data:
        result.append(list(map(int, d.split(" "))))

    return result


def get_next_line(line):
    is_zero = True
    for l in line:
        if l != 0:
            is_zero = False
            break
    if is_zero:
        return 0

    differences = [line[x+1]-line[x] for x in range(len(line)-1)]
    prev_line_result = get_next_line(differences)

    return line[-1] + prev_line_result


def get_next_line_pt2(line):
    is_zero = True
    for l in line:
        if l != 0:
            is_zero = False
            break
    if is_zero:
        return 0

    differences = [line[x+1]-line[x] for x in range(len(line)-1)]
    prev_line_result = get_next_line_pt2(differences)

    return line[0] - prev_line_result


def solve(data):
    s = 0
    for l in data:
        s += get_next_line_pt2(l)

    print(s)
    pass


if __name__ == '__main__':
    data = read_data()
    solve(data)
