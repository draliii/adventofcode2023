import copy
import hashlib


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


if __name__ == '__main__':
    data = read_data()
    print(solve(data))
