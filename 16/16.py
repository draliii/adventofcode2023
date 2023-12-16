def read_data():
    pt1 = False
    f = open("16-full.in", "r")
    f = open("16.in", "r")
    data = f.read().split("\n")
    return data


def solve(data):
    hash_value = 0
    for word in data:
        hash_value += hash(word)
    return hash_value


if __name__ == '__main__':
    data = read_data()
    print(solve(data))
    #print(solve_v2(data))
