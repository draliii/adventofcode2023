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


def solve_line(condition, numbers, idx):
    if len(condition) == 0:
        if idx >= len(numbers):
            return 1
        else:
            return 0

    c = condition[0]
    if c == ".":
        # tady cislo urcite nezacina, muzu jit dal
        return solve_line(condition[1:], numbers, idx)
    if c == "#":
        # co kdyz tady zacina cislo?

        # pokud uz mi zadna cisla nezbyvaji, koncim
        if len(numbers) == idx:
            return 0

        n = numbers[idx]
        # pokud mam velke cislo, ale kratky string, taky koncim
        if len(condition) < n:
            return 0

        # musim se ujistit, ze tam nikde nemam tecky
        for i in range(0, n):
            if condition[i] == ".":
                return 0

        # ale musim se ujistit, ze tam je tecka nebo konec slova!
        newc = condition[n:]
        if len(condition) > n:
            if condition[n] == "#":
                # cislo je moc dlouhe, nemuzu ho uznat
                return 0
            if condition[n] == "?":
                newc = "." + condition[n+1:]

        # muzu pouzit to cislo a jit dal:
        return solve_line(newc, numbers, idx+1)

    # kdyz to neni ani . ani #, tak to musi byt ?, vyzkousim obe varianty
    c1 = "." + condition[1:]
    c2 = "#" + condition[1:]
    v1 = solve_line(c1, numbers, idx)
    v2 = solve_line(c2, numbers, idx)
    return v1 + v2


def solve(data):
    summ = 0
    i = 0
    for line, numbers in data:
        result = solve_line(line, numbers, 0)
        print(i, result)
        summ += result
        i+= 1
    return summ


if __name__ == '__main__':
    data = read_data()
    print(solve(data))
