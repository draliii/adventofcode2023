def read_data():
    f = open("4-full.in", "r")
    data = f.read().split("\n")

    cards = []
    for l in data:
        numbers = l.split(":")[1]
        winning, mine = numbers.split("|")
        winning = set(map(int, ' '.join(winning.split()).split(" ")))
        mine = set(map(int, ' '.join(mine.split()).split(" ")))
        cards.append([winning, mine])

    return cards


def solve(cards):
    score = 0
    card_counts = [1] * len(cards)
    i = -1
    for w, m in cards:
        i += 1
        intersect = list(list(w & m))
        isize = len(intersect)
        if isize == 0:
            continue
        score += 2 ** (isize-1)
        card_power = card_counts[i]
        for j in range(1, isize+1):
            try:
                card_counts[i+j] += card_power
            except IndexError:
                pass


    return score, card_counts


if __name__ == '__main__':
    cards = read_data()
    pt1, pt2 = solve(cards)
    print(pt2)
    sumpt2 = 0
    for i in pt2:
        sumpt2 += i
    print(sumpt2)


