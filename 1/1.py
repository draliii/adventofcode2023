import re


def read_data():
    f = open("1-full.in", "r")
    data = f.read().split("\n")
    return data


def get_first_digit(line, front=True):
    if not front:
        line = line[::-1]

    for i in range(0, len(line)):

        if i >= len(line):
            return None

        line = replace_digit(line, i, front=front)
        c = line[i]

        try:
            int(c)
            return c
        except ValueError:
            continue
    return None


def replace_digit(line, idx, front=True):
    digits_front = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    digits_back = ["eno", "owt", "eerht", "ruof", "evif", "xis", "neves", "thgie", "enin"]
    digits_int = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    if front:
        digits = digits_front
    else:
        digits = digits_back

    for d, di in zip(digits, digits_int):
        if line[idx:].startswith(d):
            line = line[:idx] + di + line[idx+1:]
            for i in range(1, len(d)):
                line = line[:idx+i] + "q" + line[idx+i+1:]

    return line


def run(data):
    number_data = []
    for l in data:
        if len(l) == 0:
            continue
        number_data.append(re.sub('[a-z]', '', l))

    result = 0
    for i, nd in enumerate(number_data):
        a = nd[0]
        b = nd[-1]
        result += int(a + b)
    return result


def run_pt2(data):

    result = 0

    for l in data:
        if len(l) == 0:
            continue
        a = get_first_digit(l)
        b = get_first_digit(l, front=False)

        print(a, l, b)

        result += int(a + b)
    return result


if __name__ == '__main__':
    data = read_data()
    print(run_pt2(data))


