def read_data():
    pt1 = False
    f = open("20-full.in", "r")
    f = open("20-triple-full.in", "r")  # 3x3 grid
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
    steps = 671
    for i in range(0, steps+1):
        position = step(stones, position)
        #print_grid(position)

    posibilities_center = count_possibilities_in_square(position, "center")
    posibilities_left = count_possibilities_in_square(position, "leftA")
    posibilities_right = count_possibilities_in_square(position, "rightA")
    posibilities_top = count_possibilities_in_square(position, "topA")
    posibilities_down = count_possibilities_in_square(position, "downA")
    posibilities_topleft = count_possibilities_in_square(position, "topleftA")
    posibilities_downleft = count_possibilities_in_square(position, "downleftA")
    posibilities_topright = count_possibilities_in_square(position, "toprightA")
    posibilities_downright = count_possibilities_in_square(position, "downrightA")
    posibilities_topleftB = count_possibilities_in_square(position, "topleftB")
    posibilities_downleftB = count_possibilities_in_square(position, "downleftB")
    posibilities_toprightB = count_possibilities_in_square(position, "toprightB")
    posibilities_downrightB = count_possibilities_in_square(position, "downrightB")
    print("=======================")
    print("step " + str(steps), posibilities_center, posibilities_left, posibilities_right, posibilities_top, posibilities_down,
          posibilities_topleft, posibilities_downleft, posibilities_topright, posibilities_downright,
          "B:", posibilities_topleftB, posibilities_downleftB, posibilities_toprightB, posibilities_downrightB)

    print("center: ", posibilities_center)
    print("leftA: ", posibilities_left)
    print("rightA: ", posibilities_right)
    print("topA: ", posibilities_top)
    print("downA: ", posibilities_down)
    print("topleftA: ", posibilities_topleft)
    print("downleftA: ", posibilities_downleft)
    print("toprightA: ", posibilities_topleft)
    print("downrightA: ", posibilities_downright)
    print("topleftB: ", posibilities_topleftB)
    print("downleftB: ", posibilities_downleftB)
    print("toprightB: ", posibilities_toprightB)
    print("downrightB: ", posibilities_downrightB)


def calculate_result(k, purple_coef, green_coef, blue_coef, orange_coef):
    s = (2*k+1)*(2*k+1)

    b_count = (s-1)/2
    a_count = b_count + 1

    blue_count = b_count/2
    orange_count = blue_count

    # sudy pocet kroku
    if k%2 == 0:
        purple_count = k*k
        green_count = a_count - purple_count
    else:
        green_count = k*k
        purple_count = a_count - green_count

    print(purple_count, green_count, blue_count, orange)
    result = purple_coef * purple_count + green_coef * green_count + blue_coef * blue_count + orange_coef * orange
    return result


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


def count_possibilities_in_square(position, name):
    result = 0
    K = len(position)

    # default to center
    top_left_size, top_right_size, down_left_size, down_right_size = (327, 327, 327, 327)

    if name == "centerA":
        top_left_size, top_right_size, down_left_size, down_right_size = (327, 327, 327, 327)
    elif name == "leftA":
        top_left_size, top_right_size, down_left_size, down_right_size = (196, 458, 196, 458)
    elif name == "rightA":
        top_left_size, top_right_size, down_left_size, down_right_size = (458, 196, 458, 196)
    elif name == "downA":
        top_left_size, top_right_size, down_left_size, down_right_size = (458, 458, 196, 196)
    elif name == "topA":
        top_left_size, top_right_size, down_left_size, down_right_size = (196, 196, 458, 458)
    elif name == "topleftA":
        top_left_size, top_right_size, down_left_size, down_right_size = (65, 327, 327, 589)
    elif name == "downleftA":
        top_left_size, top_right_size, down_left_size, down_right_size = (327, 589, 65, 327)
    elif name == "toprightA":
        top_left_size, top_right_size, down_left_size, down_right_size = (327, 65, 589, 327)
    elif name == "downrightA":
        top_left_size, top_right_size, down_left_size, down_right_size = (589, 327, 327, 65)
    elif name == "topleftB":
        top_left_size, top_right_size, down_left_size, down_right_size = (196, 327, 327, 458)
    elif name == "downleftB":
        top_left_size, top_right_size, down_left_size, down_right_size = (327, 458, 196, 327)
    elif name == "toprightB":
        top_left_size, top_right_size, down_left_size, down_right_size = (327, 196, 458, 327)
    elif name == "downrightB":
        top_left_size, top_right_size, down_left_size, down_right_size = (458, 327, 327, 196)

    grid = new_grid(K, K, 0)
    for i in range(K):
        for j in range(K):
            isA = True
            if i + j < top_left_size:
                isA = False
            elif (K - i - 1) + (K - j - 1) < down_right_size:
                isA = False
            elif i + (K - j - 1) < top_right_size:
                isA = False
            elif (K - i - 1) + j < down_left_size:
                isA = False

            if isA:
                result += position[i][j]
                grid[i][j] += 1

    # print_grid(grid)
    return result


def count_possibilities(position):
    result = 0
    for i in range(len(position)):
        result += sum(position[i])

    return result


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


def test_calculation():
    green = 3787
    purple = 3748
    blue = 3801
    orange = 3739
    k = 2

    k2_correct_solution = 9*green + 6*blue + 6*orange + 4*purple
    k2_calculated_solution = int(calculate_result(k, purple, green, blue, orange))
    assert(k2_correct_solution == k2_calculated_solution)

    k = 3
    k3_correct_solution = 9*green + 12*blue + 12*orange + 16*purple
    k3_calculated_solution = int(calculate_result(k, purple, green, blue, orange))
    assert(k3_correct_solution == k3_calculated_solution)

    k = 4
    k4_correct_solution = 25*green + 20*blue + 20*orange + 16*purple
    print(purple, green, blue, orange)
    k4_calculated_solution = int(calculate_result(k, purple, green, blue, orange))
    assert(k4_correct_solution == k4_calculated_solution)


if __name__ == '__main__':
    data = read_data()
    purple, green, blue, orange = 3748, 3787, 3801, 3739  # obtained from calculating steps in each cell on an even step

    # The final step 26501365 can be expressed as 65 + 131*202300, where 65 is num.steps to edge of the center cell
    # and 131 is the width of the grid. The number 202300 defines the final grid size, which can be used to calculate
    # cell types and therefore sum all possible steps
    print(calculate_result(202300, purple, green, blue, orange))

    # test_calculation()
    # print(solve(*data))
