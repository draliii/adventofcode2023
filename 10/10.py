import numpy as np

def read_data():
    f = open("10-full.in", "r")
    #f = open("10.in", "r")
    #f = open("10-pt2.in", "r")
    data = f.read().split("\n")

    pipe_height = len(data)
    pipe_width = len(data[0])

    pipes = np.zeros((pipe_height*3, pipe_width*3), dtype=np.int32)

    shapes = {
    "|": np.array([[0, 1, 0], [0, -1, 0], [0, 1, 0]]),
    "-": np.array([[0, 0, 0], [1, -1, 1], [0, 0, 0]]),
    "L": np.array([[0, 1, 0], [0, -1, 1], [0, 0, 0]]),
    "J": np.array([[0, 1, 0], [1, -1, 0], [0, 0, 0]]),
    "7": np.array([[0, 0, 0], [1, -1, 0], [0, 1, 0]]),
    "F": np.array([[0, 0, 0], [0, -1, 1], [0, 1, 0]]),
    "S": np.array([[0, 0, 0], [0, 10, 0], [0, 0, 0]]),
    ".": np.array([[0, 0, 0], [0, -1, 0], [0, 0, 0]])}

    startr = 0
    startc = 0

    for r in range(pipe_height):
        for c in range(pipe_width):
            pipe_shape = data[r][c]
            if pipe_shape == "S":
                startr = 3*r + 1
                startc = 3*c + 1
            R = r*3
            C = c*3
            pipes[R:R+3, C:C+3] = shapes[pipe_shape]

    if pipes[startr-2, startc] == 1:
        pipes[startr-1, startc] = 1
    if pipes[startr+2, startc] == 1:
        pipes[startr+1, startc] = 1
    if pipes[startr, startc-2] == 1:
        pipes[startr, startc-1] = 1
    if pipes[startr, startc+2] == 1:
        pipes[startr, startc+1] = 1

    return pipes, startr, startc

def flood_fill(data, start, value):
    # rucne, protoze se mi nechce instalovat scikit-image
    
    queue = [start]
    while True:
        if len(queue) == 0:
            return

        x, y = queue.pop(0)
        old_value = data[x, y]
        if old_value == value:
            continue

        data[x, y] = value

        for xdif, ydif in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            X = x + xdif
            Y = y + ydif
            if X < 0 or Y < 0 or X >= data.shape[0] or Y >= data.shape[1]:
                continue
            if data[X, Y] == old_value:
                queue.append((X, Y))





def do_step(data, r, c, x, y):
    step = data[r + x, c + y]
    distance = data[r, c]

    if step == 0:
        # chci jit jinam, tohle neni dobry smer
        return False, distance

    if step == -1:
        # tohle je stred, pricitam
        new_distance = distance + 10
        data[r + x, c + y] = new_distance
        return True, new_distance

    if step == 1:
        # tohle je cesta, jdu tudy a nic neresim
        data[r + x, c + y] = distance
        return True, distance

    return False, distance


def solve(data, startr, startc):
    r = startr
    c = startc
    # data[r, c] = 0
    max_distance = 0
    while True:
        moved = False
        for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            result, distance = do_step(data, r, c, x, y)
            if distance > max_distance:
                max_distance = distance
            if result:
                r += x
                c += y
                moved = True
                break
        if not moved:
            break
    print(int((max_distance)/20))
    k = 3

    # replace all ones (unused tiles) with zeros (ground)
    data = np.where(data == 1, 0, data)

    k=3

    # flood the outside with -1s, replacing all zeros with -1
    flood_fill(data, (0, 0), -1)
    print(k)

    k=3

    # flood the outside with 0s, replacing all the outside with zeros
    flood_fill(data, (0, 0), 0)
    print(k)

    k=3

    # replace all remaining -1s (on the inside) with ones and delete all other data
    data = np.where(data == -1, 1, 0)

    # sum all ones, this is the number of enclosed tiles
    print(np.sum(data))


if __name__ == '__main__':
    data, startr, startc = read_data()
    solve(data, startr, startc)
