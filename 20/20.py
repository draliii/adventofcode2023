def read_data():
    pt1 = False
    f = open("20-full.in", "r")
    f = open("20-triple-full.in", "r")
    #f = open("20.in", "r")
    data = f.read().split("\n")
    stones = new_grid(len(data[0]), len(data), 0)
    positions = new_grid(len(data[0]), len(data), 0)

    for i in range(len(data)):
        for j in range(len(data[0])):
            tile = data[i][j]
            if tile == "S":
                positions[i][j] = 1
            if tile == "#":
                stones[i][j] = 1

    return stones, positions


def solve(stones, position):
    steps = 200
    for i in range(0, steps):
        position = step(stones, position)
        #print_grid(position)

        # print(count_possibilities(position))
        posibilities = count_possibilities_in_A(position)
        print(i, posibilities)
        mm = magic_math(posibilities, 3748)
        if mm != 0:
            print(mm)
        mm = magic_math(posibilities, 3787)
        if mm != 0:
            print(mm)


def step(stones, position):
    new_postition = new_grid(len(stones[0]), len(stones), 0)
    for i in range(len(stones)):
        for j in range(len(stones[0])):
            if position[i][j]:
                iss = []
                if i > 0:
                    iss.append((i-1, j))
                if i < len(stones)-1:
                    iss.append((i+1, j))
                if j > 0:
                    iss.append((i, j-1))
                if j < len(stones[0])-1:
                    iss.append((i, j+1))
                for x, y in iss:
                    if not stones[x][y]:
                        new_postition[x][y] = 1
    return new_postition


def count_possibilities_in_A(position):
    result = 0
    K = len(position)
    corner_size = 196
    #corner_size = 65
    grid = new_grid(K, K, 0)
    for i in range(K):
        for j in range(K):
            if i + j < corner_size:
                continue
            if (K - i - 1) + (K - j - 1) < corner_size:
                continue
            if i + (K - j - 1) < corner_size:
                continue
            if (K - i - 1) + j < corner_size:
                continue
            result += position[i][j]
            grid[i][j] = 1

    #print_grid(grid)
    return result

def count_possibilities(position):
    result = 0
    for i in range(len(position)):
        result += sum(position[i])

    return result


def magic_math(all_sum, A):
    if (all_sum - 5*A) % 4 != 0:
        return 0
    alpha = (all_sum - 5*A) / 4
    return 81850984600.0 * alpha + 81850984601*A


def new_grid(width, height, default_value = 0):
    grid = []
    for x in range(0, height):
        line = [default_value] * width
        grid.append(line)
    return grid

def print_grid(grid):
    for i in range(len(grid)):
        print(''.join(map(str, grid[i])))
    print()



if __name__ == '__main__':
    data = read_data()
    print(solve(*data))
