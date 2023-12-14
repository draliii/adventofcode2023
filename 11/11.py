import numpy as np

def read_data():
    f = open("11-full.in", "r")
    #f = open("11.in", "r")
    data = f.read().split("\n")
    return data


def solve(data):
    pass


if __name__ == '__main__':
    data = read_data()
    solve(data)
