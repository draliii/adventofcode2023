import math


def read_data():
    pt1 = False
    f = open("24-full.in", "r")
    # f = open("24.in", "r")
    data = f.read().split("\n")
    positions, directions = [], []
    for d in data:
        nums = d.replace(",", "").replace("  ", " ").split(" ")
        position = list(map(int, nums[0:3]))
        direction = list(map(int, nums[4:]))
        positions.append(position)
        directions.append(direction)
    return positions, directions


def solve(positions, directions):
    collisions = 0
    N = len(positions)
    planes = []
    for i in range(0, N):
        for j in range(i + 1, N):
            if i == 12 and j == 188:
                k = 3
            intersection = list(get_intersect(positions[i], directions[i], positions[j], directions[j]))
            if intersection[0] is None:
                continue
            v = get_plane_v2(positions[i], positions[j], intersection)
            planes.append((v, intersection))
    print(planes)

    return collisions


def foo(pa, va, pb, vb):
    ga = math.gcd(*va)
    gb = math.gcd(*vb)

    if ga != 1:
        va = list(map(lambda x: x / ga, va))
    if gb != 1:
        vb = list(map(lambda x: x / gb, vb))

    if (abs(va[0]) == abs(vb[0])):
        if (abs(va[1]) == abs(vb[1])):
            print(va, vb)
            return True

    return False


def intersect(pa, va, pb, vb):
    # m = (pb[1]*va[0]-pa[1]*pb[0]+pa[1]*pa[0])/(pa[1]*vb[0] - vb[1]*va[0])
    top = (pb[1] * va[0] - pa[1] * va[0] - va[1] * pb[0] + pa[0] * va[1])
    bottom = (va[1] * vb[0] - vb[1] * va[0])
    if bottom == 0 or va[0] == 0:
        return False
    m = top / bottom
    t = (pb[0] + vb[0] * m - pa[0]) / va[0]

    if m < 0 or t < 0:
        return False

    x = pa[0] + t * va[0]
    y = pa[1] + t * va[1]

    mmin = 200000000000000
    mmax = 400000000000000

    if mmin < x < mmax and mmin < y < mmax:
        return True
    return False


def get_plane(M, N, O):
    x1, y1, z1 = M
    x2, y2, z2 = N
    x3, y3, z3 = O

    top = y2*z3 - y1*z3 - y3*z2 - y3*z1 - y2*z2 + y1*z2
    bottom = x3*y2 - x3*y1 - x2*y3 + x1*y3 - x1*y2 + x1*y1 + x2*y1 - x1*y1
    a = top/bottom
    b = (z2 - a*x2 - z1 + a*x1)/(y2-y1)
    c = z1 - a*x1 - b*y1

    return a, b, c


def get_plane_v2(start1, start2, intersection):
    A = list(map(lambda x: x[0] - x[1], zip(start1, intersection)))
    B = list(map(lambda x: x[0] - x[1], zip(start2, intersection)))

    a1, a2, a3 = A
    b1, b2, b3 = B

    s1 = a2*b3 - a3*b2
    s2 = a3*b1 - a1*b3
    s3 = a1*b2 - a2*b1

    return s1, s2, s3


def get_intersect(pa, va, pb, vb):
    top = (pb[1] * va[0] - pa[1] * va[0] - va[1] * pb[0] + pa[0] * va[1])
    bottom = (va[1] * vb[0] - vb[1] * va[0])
    if bottom == 0 or va[0] == 0:
        return None, None, None
    m = top / bottom
    t = (pb[0] + vb[0] * m - pa[0]) / va[0]

    x = pa[0] + t * va[0]
    y = pa[1] + t * va[1]

    za = pa[2] + t * va[2]
    zb = pa[2] + m * va[2]

    if za == zb:
        return x, y, za

    return None, None, None


def intersect_planes(vector1, point1, vector2, point2):
    pass



if __name__ == '__main__':
    data = read_data()
    print(solve(*data))
