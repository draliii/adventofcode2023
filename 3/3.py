def read_data():
    f = open("3-full.in", "r")
    data = f.read().split("\n")

    grid = [["."] * (len(data[0]) + 2)]
    gears = [[0] * (len(data[0]) + 2)]
    gears_multi = [[1] * (len(data[0]) + 2)]
    for l in data:
        gridline = "." + l + "."
        grid.append(list(gridline))
        gears.append([0]*len(gridline))
        gears_multi.append([1]*len(gridline))
    grid.append(["."] * (len(data[0]) + 2))
    gears.append([0] * (len(data[0]) + 2))
    gears_multi.append([1] * (len(data[0]) + 2))

    return grid, gears, gears_multi


def solve(grid, gears, gears_multi):
    result = 0

    is_number = False
    number_start = 0
    number_size = 0

    for ri, row in enumerate(grid):
        for ci, element in enumerate(row):
            try:
                i = int(element)
                if not is_number:
                    is_number = True
                    number_start = [ri, ci]
                number_size += 1
            except ValueError:
                if is_number:
                    number = int(''.join(row[number_start[1]:number_start[1] + number_size]))
                    is_part = find_symbols(grid, number_start[0], number_start[1], number_size, gears, gears_multi, number)

                    if is_part:
                        result += number
                    is_number = False
                    number_size = 0

    return result


def is_char(grid, ri, ci, gears, gears_multi, number):
    c = grid[ri][ci]
    try:
        int(c)
        return False
    except ValueError:
        pass
    if c == ".":
        return False
    if c == "*":
        gears[ri][ci] += 1
        gears_multi[ri][ci] *= number
    return True


def find_symbols(grid, row, col, size, gears, gears_multi, number):
    result = False
    if is_char(grid, row, col-1, gears, gears_multi, number):
        result = True
    if is_char(grid, row, col+size, gears, gears_multi, number):
        result = True
    for ci in range(col-1, col+size+1):
        if is_char(grid, row-1, ci, gears, gears_multi, number):
            result = True
        if is_char(grid, row+1, ci, gears, gears_multi, number):
            result = True
    return result


def find_gears(gears, gears_multi):
    result = 0
    for ri, r in enumerate(gears):
        for ci, e in enumerate(r):
            if e == 2:
                result += gears_multi[ri][ci]
    return result


if __name__ == '__main__':
    gridd, gearss, gears_multii = read_data()
    print(solve(gridd, gearss, gears_multii))
    print(find_gears(gearss, gears_multii))

