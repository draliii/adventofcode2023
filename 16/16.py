def read_data():
    pt1 = False
    f = open("16-full.in", "r")
    # f = open("16.in", "r")
    data = f.read().split("\n")
    return data


def get_direction(direction):

    if direction == "up":
        ray_rowstep = -1
        ray_colstep = 0

    if direction == "down":
        ray_rowstep = 1
        ray_colstep = 0

    if direction == "left":
        ray_rowstep = 0
        ray_colstep = -1

    if direction == "right":
        ray_rowstep = 0
        ray_colstep = 1

    return ray_rowstep, ray_colstep


def solve(data, rays_trace, start):
    rays = [start]

    while True:
        if len(rays) == 0:
            break
        ray = rays.pop()
        ray_row = ray[0]
        ray_col = ray[1]
        direction = ray[2]
        ray_rowstep, ray_colstep = get_direction(direction)

        nr = ray_row + ray_rowstep
        nc = ray_col + ray_colstep

        # ten paprsek uz tady byl, skip
        if rays_trace[direction][ray_row][ray_col]:
            continue

        # oznac puvodni pole, ze uz jsem tam byla
        if not (ray_row >= len(data) or ray_row < 0 or ray_col >= len(data[0]) or ray_col < 0):
            rays_trace[direction][ray_row][ray_col] = 1

        if nr >= len(data) or nr < 0 or nc >= len(data[0]) or nc < 0:
            continue

        tile = data[nr][nc]

        if tile == ".":
            rays.append([nr, nc, direction])
            continue

        if tile == "-":
            if direction == "left" or direction == "right":
                # pass through:
                rays.append([nr, nc, direction])
            else:
                # split:
                rays.append([nr, nc, "left"])
                rays.append([nr, nc, "right"])
            continue

        if tile == "|":
            if direction == "up" or direction == "down":
                # pass through:
                rays.append([nr, nc, direction])
            else:
                # split:
                rays.append([nr, nc, "up"])
                rays.append([nr, nc, "down"])
            continue

        if tile == "/":
            if direction == "up":
                nd = "right"
            elif direction == "right":
                nd = "up"
            elif direction == "left":
                nd = "down"
            else:
                nd = "left"
            rays.append([nr, nc, nd])

        if tile == "\\":
            if direction == "up":
                nd = "left"
            elif direction == "left":
                nd = "up"
            elif direction == "right":
                nd = "down"
            else:
                nd = "right"
            rays.append([nr, nc, nd])

    energized = new_array(len(data), len(data[0]))
    energized_sum = 0
    for r in range(len(data)):
        for c in range(len(data[0])):
            s = rays_trace["down"][r][c] + rays_trace["up"][r][c] + rays_trace["left"][r][c] + rays_trace["right"][r][c]
            if s > 0:
                energized[r][c] = 1
                energized_sum += 1

    return energized_sum


def get_new_rays_trace(data):
    rays_trace = {}
    for direction in ["left", "right", "up", "down"]:
        rays_trace[direction] = new_array(len(data), len(data[0]))
    return rays_trace


def solve_pt2(data):
    best = 0

    for i in range(0, len(data)):
        rays_trace = get_new_rays_trace(data)
        result = solve(data, rays_trace, [i, 0, "right"])
        if result > best:
            print(i, "right", result)
            best = result

        rays_trace = get_new_rays_trace(data)
        result = solve(data, rays_trace, [i, len(data[0])-1, "left"])
        if result > best:
            print(i, "left", result)
            best = result

    for j in range(0, len(data[1])):
        rays_trace = get_new_rays_trace(data)
        result = solve(data, rays_trace, [0, j, "down"])
        if result > best:
            print(j, "down", result)
            best = result

        rays_trace = get_new_rays_trace(data)
        result = solve(data, rays_trace, [len(data)-1, j, "up"])
        if result > best:
            print(j, "up", result)
            best = result

    return best



def new_array(rows, cols):
    array = []
    for i in range(rows):
        a = [0] * cols
        array.append(a)
    return array


if __name__ == '__main__':
    data = read_data()

    ray_traces = get_new_rays_trace(data)

    print(solve(data, ray_traces, (0, -1, "right")))

    print(solve_pt2(data))
