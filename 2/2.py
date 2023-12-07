def check_round(colors):
    for color in colors.split(","):
        color = color.strip()
        num, c = color.split(" ")
        if int(num) > limits[c]:
            return False
    return True


def check_round_pt2(colors, mins):
    for color in colors.split(","):
        color = color.strip()
        num, c = color.split(" ")
        if int(num) > mins[c]:
            mins[c] = int(num)
    return mins


f = open("2-full.in", "r")
data = f.read().split("\n")

limits = {"red": 12, "green": 13, "blue": 14}
result = 0

for i, game in enumerate(data):
    if len(game) == 0:
        continue
    values = game.split(":")[1]
    mins = {"red": 0, "green": 0, "blue": 0}

    for v in values.split(";"):
        v = v.strip()
        mins = check_round_pt2(v, mins)

    power = mins["red"]*mins["blue"]*mins["green"]
    result += power

print(result)

