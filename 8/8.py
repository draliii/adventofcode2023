from math import lcm

def read_data():
    f = open("8-full.in", "r")
    # f = open("8.in", "r")
    # f = open("8-pt2.in", "r")
    data = f.read().split("\n")

    instructions = list(map(lambda x: int((ord(x)-76)/6), data[0]))

    graph_lines = data[2:]

    graph = {}
    starts = []
    for gl in graph_lines:
        nodes = gl.split(" ")
        graph[nodes[0]] = [nodes[2][1:-1], nodes[3][:-1]]
        if nodes[0].endswith("A"):
            starts.append(nodes[0])

    return instructions, graph, starts


def walk(graph, step, instuctions):
    ends = []
    for i, instruction in enumerate(instuctions):
        if step.endswith("Z"):
            ends.append(i)
        step = graph[step][instruction]
    return step, ends


def convert_instructions(line):
    # r = 82
    # l = 76
    # prevadi L a R na cisla 0 a 1 s vyuzitim jejich ascii hodnot
    return list(map(lambda x: int((int(x)-76)/6), line))


def getinstruction(inp="str"):
    i = -1
    l = len(inp)
    while True:
        i += 1
        if i == l:
            i = 0
        yield i, inp[i]



def solve(graph, instructions, step):
    for i, gg in enumerate(getinstruction(instructions)):
        j, g = gg
        print(step)
        # is this the last step?
        #if "ZZZ" in step:
        #    return i
        is_last = True
        for s in step:
            if not s.endswith("Z"):
                is_last = False
                break
        if is_last:
            return i

        next_step = []

        for node in step:
            next_step.append(graph[node][g])

        step = next_step


def solve_v2(graph, instructions, starts):
    periods = []
    for s in starts:
        offset, period = get_period(graph, instructions, s)
        print(offset, period)
        periods.append(period)

    print(lcm(*periods))


def get_period(graph, instructions, step):
    ends = {}

    for step_counter, gg in enumerate(getinstruction(instructions)):
        instruction_counter, instruction = gg

        if step.endswith("Z"):

            if step not in ends:
                ends[step] = {}

            if instruction_counter in ends[step]:
                previous_hit = ends[step][instruction_counter]
                return step_counter, step_counter - previous_hit
            else:
                ends[step][instruction_counter] = step_counter

        step = graph[step][instruction]


if __name__ == '__main__':
    instructions, graph, starts = read_data()
    solve_v2(graph, instructions, starts)

    # print(solve(graph, instructions, starts))
