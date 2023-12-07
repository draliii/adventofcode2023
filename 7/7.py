def read_data():
    f = open("7-full.in", "r")
    # f = open("7.in", "r")
    data = f.read().split("\n")

    games = []
    for l in data:
        if len(l) == 0:
            continue
        games.append(l.split(" "))

    return games


def card_to_num(c, pt2=False):
    if pt2:
        mapping = {"A": 12, "K": 11, "Q": 10, "J": 0, "T": 9, "9": 8, "8": 7, "7": 6, "6": 5, "5": 4, "4": 3, "3": 2,
                   "2": 1}
    else:
        mapping = {"A": 12, "K": 11, "Q": 10, "J": 9, "T": 8, "9": 7, "8": 6, "7": 5, "6": 4, "5": 3, "4": 2, "3": 1,
                   "2": 0}

    return mapping[c]


def get_hand_value(cards, rank, pt2=False):
    value = 0
    cards = cards[::-1]
    for i, c in enumerate(cards):
        value += card_to_num(c, pt2=pt2) * (13 ** i)
    value += rank * (13 ** 5)
    return value


def get_hand_rank(g, pt2=False):

    cards = {e:g.count(e) for e in set(g)}

    if not pt2:
        j_count = 0
    else:
        try:
            j_count = cards["J"]
            cards["J"] = 0
        except KeyError:
            j_count = 0

    counts = list(cards.values())
    counts.sort(reverse=True)

    # 5, 4, 3+2, 3, 2+2, 2, unique
    # 6, 5,   4, 3,   2, 1,      0

    rank = 0

    if g == "9999J" or g == "JJJJJ":
        k = 3

    if counts[0]+j_count == 5:
        rank = 6
    elif counts[0]+j_count == 4:
        rank = 5
    elif counts[0]+j_count == 3:
        if counts[1] == 2:
            rank = 4
        else:
            rank = 3
    elif counts[0]+j_count == 2:
        if counts[1] == 2:
            rank = 2
        else:
            rank = 1
    else:
        rank = 0

    return rank


def process_hand(g, pt2=False):
    rank = get_hand_rank(g, pt2=pt2)
    value = get_hand_value(g, rank, pt2=pt2)
    return value


def solve(games):
    for g in games:
        game_value = process_hand(g[0], pt2=True)
        g.append(game_value)

    games.sort(key=lambda x: x[2])

    sum = 0
    for i, g in enumerate(games):
        sum += (i+1) * int(g[1])

    print(games)
    print(sum)

    for g in games:
        print(g[0], g[2])


if __name__ == '__main__':
    games = read_data()
    solve(games)
