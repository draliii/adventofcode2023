def read_data():
    pt1 = False
    f = open("15-full.in", "r")
    # f = open("15.in", "r")
    data = f.read().split("\n")
    data = data[0].split(",")

    return data


def hash(part):
    result = 0
    for c in part:
        i = ord(c)
        result = result + i
        result = result * 17
        result = result % 256
    return result


def solve(data):
    hash_value = 0
    for word in data:
        hash_value += hash(word)
    return hash_value


def solve_v2(data):
    hashmap = []
    for i in range(256):
        hashmap.append({})

    for word in data:
        if "=" in word:
            label, focus = word.split("=")
            box_id = hash(label)
            hashmap[box_id][label] = focus
        if "-" in word:
            label = word.split("-")[0]
            box_id = hash(label)
            if label in hashmap[box_id]:
                hashmap[box_id].pop(label)

    result = 0
    for box_id in range(256):
        for i, k in enumerate(hashmap[box_id].keys()):
            result += (box_id + 1) * (i + 1) * int(hashmap[box_id][k])

    return result


if __name__ == '__main__':
    data = read_data()
    print(solve(data))
    print(solve_v2(data))
