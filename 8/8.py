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
    return list(map(lambda x: int((int(x)-76)/6), line))


def getinstruction(inp="str"):
    i = -1
    l = len(inp)
    while True:
        i += 1
        if i == l:
            i = 0
        yield (inp[i])


def solve(graph, instructions, step):
    for i, g in enumerate(getinstruction(instructions)):
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


def get_period(graph, instructions, step):
    ends = []
    end_indices = []

    for i, g in enumerate(getinstruction(instructions)):
        if step.endswith("Z"):
            ends.append(step)
            end_indices.append(i)



        step = graph[step][g]





if __name__ == '__main__':
    instructions, graph, starts = read_data()
    print(solve(graph, instructions, starts))
