CACHE = {}

def read_data():
    pt1 = False
    f = open("12-full.in", "r")
    f = open("12.in", "r")
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


def solve_line(condition, str_idx, numbers, idx):
    if str_idx >= len(condition):
        if idx >= len(numbers):
            return 1
        else:
            return 0

    c = condition[str_idx]
    if c == ".":
        # tady cislo urcite nezacina, muzu jit dal
        return solve_line(condition, str_idx+1, numbers, idx)
    if c == "#":
        return solve_line_start_here(condition, str_idx, numbers, idx)

    # kdyz to neni ani . ani #, tak to musi byt ?, vyzkousim obe varianty
    if str_idx == 6 and condition == "?###????????":
        k = 3
    v1 = solve_line(condition, str_idx+1, numbers, idx)
    v2 = solve_line_start_here(condition, str_idx, numbers, idx)
    return v1 + v2


def solve_line_start_here(condition, str_idx, numbers, idx):
    # tady zacina cislo

    # pokud uz mi zadna cisla nezbyvaji, koncim
    if len(numbers) == idx:
        return 0

    n = numbers[idx]
    # pokud mam velke cislo, ale kratky string, taky koncim
    if len(condition) - str_idx < n:
        return 0

    # musim se ujistit, ze tam nikde nemam tecky
    for i in range(0, n):
        if condition[str_idx + i] == ".":
            return 0

    # ale musim se ujistit, ze tam je tecka nebo konec slova!
    if len(condition) - str_idx == n:
        # krizky vyplnuji vse az do konce slova
        # pokud to neni posledni cislo, tak koncim!
        if len(numbers) - idx > 1:
            return 0
        return 1

    if len(condition) - str_idx > n:
        if condition[str_idx + n] == "#":
            # cislo je moc dlouhe, nemuzu ho uznat
            return 0
        if condition[str_idx + n] == "?":
            # nemuzu tam dat ?, musi tam byt ., takze rovnou preskakuju a jdu dal
            return solve_line(condition, str_idx + n + 1, numbers, idx + 1)

    # muzu pouzit to cislo a jit dal:
    return solve_line(condition, str_idx + n, numbers, idx + 1)



def solve(data):
    summ = 0
    i = 0
    for line, numbers in data:
        result = solve_line(line, 0, numbers, 0)
        print(i, result)
        summ += result
        i+= 1
    return summ


if __name__ == '__main__':
    data = read_data()
    #solve_line("???", 0, [2, 1], 0)
    print(solve(data))
