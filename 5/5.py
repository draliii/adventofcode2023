def process_step(mappings, ranges):
    # zpracuje sadu pravidel pro vsechny vstupni rozsahy

    # pole vystupnich rozsahu, ktere se budou zpracovavat v pristim kole
    # v tomhle kole uz se zpracovat nesmi
    new_ranges = []

    # unprocessed: tyhle rozsahy jeste neprosly zadnym pravidlem
    unprocessed_ranges = ranges

    # postupne prochazim mapovani (na poradi zalezi)
    # jakmile mi nejaky kus mapovani sedne, tak si ho ulozim do vysledku
    # na nepouzite intervaly zkousim dalsi pravidla
    for m in mappings:
        unprocessed_ranges, processed_ranges = process_v2(m, unprocessed_ranges)
        new_ranges.extend(processed_ranges)
    new_ranges.extend(unprocessed_ranges)

    return new_ranges


def process_v2(mapping, ranges):
    # udrzuju dva typy poli, ty co se uz zpracovaly a na ktere nesmim sahat, a ty, ktere jeste zadnym mapovanim neprosly
    unprocessed_ranges = []
    processed_ranges = []

    #seo = start, end a offset daneho mapovani
    s, e, o = mapping

    for start, end in ranges:
        # vstup je pred zadanim, nemuzu ho pouzit
        if end < s:
            unprocessed_ranges.append([start, end])
            continue

        # vstup je za mapovanim, nemuzu ho pouzit
        if start > e:
            unprocessed_ranges.append([start, end])
            continue

        # vstup zacina driv nez mapovani
        # tj. musim cast poslat dal jeste pred zacatkem
        if start < s:
            unprocessed_ranges.append([start, s-1])

        # vstup konci pozdeji nez mapovani
        # tj. musim cast poslat dal i po konci
        if e < end:
            unprocessed_ranges.append([e+1, end])

        # plus pridam cely rozsah, ktery se prekryva s mapovanim
        s_new = max(s, start) + o
        e_new = min(e, end) + o
        processed_ranges.append([s_new, e_new])

    return unprocessed_ranges, processed_ranges


def clean_ranges(ranges):
    # smaze z rozsahu prazdna pole (vznikaji mi tam v process_v2 a delaji bordel)
    new_ranges = []
    for r in ranges:
        if len(r) != 0:
            new_ranges.append(r)
    return new_ranges


def get_best(ranges):
    # najde minimum z pole rozsahu
    min_range = ranges[0][0]
    for r in ranges[1:]:
        if r[0] < min_range:
            min_range = r[0]
    return min_range


def read_input():
    f = open("5-full.in", "r")
    lines = f.read().split("\n")

    seeds_raw = list(map(int, lines[0].split(" ")[1:]))
    seeds = []

    for i in range(0, len(seeds_raw), 2):
        start = seeds_raw[i]
        end = start + seeds_raw[i+1] - 1
        seeds.append([start, end])

    maps = []

    for l in lines[1:]:
        if len(l) == 0:
            continue
        if "map" in l:
            maps.append([])
        else:

            numbers = l.split(" ")
            destination, start, size = list(map(int, numbers))
            offset = destination - start
            end = start + size - 1

            maps[-1].append((start, end, offset))
    return seeds, maps

def read_input_pt1():
    f = open("5-full.in", "r")
    lines = f.read().split("\n")

    seeds_raw = list(map(int, lines[0].split(" ")[1:]))
    seeds = []

    for i in range(0, len(seeds_raw), 1):
        start = seeds_raw[i]
        end = start
        seeds.append([start, end])

    maps = []

    for l in lines[1:]:
        if len(l) == 0:
            continue
        if "map" in l:
            maps.append([])
        else:

            numbers = l.split(" ")
            destination, start, size = list(map(int, numbers))
            offset = destination - start
            end = start + size - 1

            maps[-1].append((start, end, offset))
    return seeds, maps


seeds, maps = read_input()

bests = []
for seed in seeds:
    ranges = [seed]
    for m in maps:
        ranges = process_step(m, ranges)
        ranges = clean_ranges(ranges)
        if seed[0] == 1931540843:
            print(ranges)
    bests.append(get_best(ranges))

print(min(bests))




