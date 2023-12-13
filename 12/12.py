def read_data():
    pt1 = False
    f = open("12-full.in", "r")
    # f = open("12.in", "r")
    data = f.read().split("\n")

    result = []
    for d in data:
        condition, numbers = d.split(" ")
        ns = list(map(int, numbers.split(",")))
        if pt1:
            result.append((condition, ns))
        else:
            condition = condition + "?" + condition + "?" + condition + "?" + condition + "?" + condition
            result.append((condition, 5*ns))

    return result


def cache_init(str_size, n_size):
    CACHE = []
    for i in range(0, str_size):
        CACHE.append([-1] * n_size)
    return CACHE


def cache_put(CACHE, str_idx, idx, solution):
    CACHE[str_idx][idx] = solution


def cache_get(CACHE, str_idx, idx):
    return CACHE[str_idx][idx]


def solve_line(CACHE, condition, str_idx, numbers, idx):
    cached = cache_get(CACHE, str_idx, idx)
    if cached >= 0:
        return cached

    if str_idx >= len(condition):
        if idx >= len(numbers):
            cache_put(CACHE, str_idx, idx, 1)
            return 1
        else:
            cache_put(CACHE, str_idx, idx, 0)
            return 0

    c = condition[str_idx]
    if c == ".":
        # tady cislo urcite nezacina, muzu jit dal
        solution = solve_line(CACHE, condition, str_idx+1, numbers, idx)
        cache_put(CACHE, str_idx, idx, solution)
        return solution
    if c == "#":
        solution = solve_line_start_here(CACHE, condition, str_idx, numbers, idx)
        cache_put(CACHE, str_idx, idx, solution)
        return solution

    # kdyz to neni ani . ani #, tak to musi byt ?, vyzkousim obe varianty
    v1 = solve_line(CACHE, condition, str_idx+1, numbers, idx)
    v2 = solve_line_start_here(CACHE, condition, str_idx, numbers, idx)
    solution = v1 + v2
    cache_put(CACHE, str_idx, idx, solution)
    return solution


def solve_line_start_here(CACHE, condition, str_idx, numbers, idx):
    cached = cache_get(CACHE, str_idx, idx)
    if cached >= 0:
        return cached

    # tady zacina cislo

    # pokud uz mi zadna cisla nezbyvaji, koncim
    if len(numbers) == idx:
        cache_put(CACHE, str_idx, idx, 0)
        return 0

    n = numbers[idx]
    # pokud mam velke cislo, ale kratky string, taky koncim
    if len(condition) - str_idx < n:
        cache_put(CACHE, str_idx, idx, 0)
        return 0

    # musim se ujistit, ze tam nikde nemam tecky
    for i in range(0, n):
        if condition[str_idx + i] == ".":
            cache_put(CACHE, str_idx, idx, 0)
            return 0

    # ale musim se ujistit, ze tam je tecka nebo konec slova!
    if len(condition) - str_idx == n:
        # krizky vyplnuji vse az do konce slova
        # pokud to neni posledni cislo, tak koncim!
        if len(numbers) - idx > 1:
            cache_put(CACHE, str_idx, idx, 0)
            return 0

        cache_put(CACHE, str_idx, idx, 1)
        return 1

    if len(condition) - str_idx > n:
        if condition[str_idx + n] == "#":
            # cislo je moc dlouhe, nemuzu ho uznat

            cache_put(CACHE, str_idx, idx, 0)
            return 0
        if condition[str_idx + n] == "?":
            # nemuzu tam dat ?, musi tam byt ., takze rovnou preskakuju a jdu dal
            solution = solve_line(CACHE, condition, str_idx + n + 1, numbers, idx + 1)
            cache_put(CACHE, str_idx, idx, solution)
            return solution

    # muzu pouzit to cislo a jit dal:
    solution = solve_line(CACHE, condition, str_idx + n, numbers, idx + 1)
    cache_put(CACHE, str_idx, idx, solution)
    return solution


def solve(data):
    summ = 0
    i = 0
    for line, numbers in data:
        CACHE = cache_init(len(line)+1, len(numbers)+1)
        result = solve_line(CACHE, line, 0, numbers, 0)
        print(i, result)
        summ += result
        i+= 1
    return summ


if __name__ == '__main__':
    data = read_data()
    print(solve(data))
