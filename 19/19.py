import json


def read_data():
    pt1 = False
    f = open("19-full.in", "r")
    # f = open("19.in", "r")
    data = f.read().split("\n")

    workflows = {}
    read_workflows = True
    parts = []
    queues = {}

    for d in data:
        if d == "":
            read_workflows = False
            continue

        if read_workflows:
            workflow, instuctions_raw = d.split("{")
            instructions = instuctions_raw[:-1].split(",")
            workflows[workflow] = instructions
            queues[workflow] = []

        else:
            part_raw = d.replace('x', '"x"').replace('m', '"m"').replace('a', '"a"').replace('s', '"s"').replace("=", ":")
            part = json.loads(part_raw)
            parts.append(part)

    return workflows, queues, parts


def add_part_to_queues(queues, w_queue, destination, part):
    append_in_dict(queues, destination, part)
    if destination != "A" and destination != "R":
        w_queue.add(destination)


def append_in_dict(dictionary, index, data):
    if index not in dictionary.keys():
        dictionary[index] = []
    dictionary[index].append(data)

def solve(workflows, queues, parts):
    queues = {"in": parts, "R": [], "A": []}
    w_queue = {"in"}

    while len(w_queue) > 0:
        print(w_queue)
        print(queues)

        workflow = w_queue.pop()
        if (len(queues[workflow])) == 0:
            continue
        w_queue.add(workflow)

        part = queues[workflow].pop()

        rules = workflows[workflow]
        for rule in rules:
            if ":" not in rule:
                destination = rule
                add_part_to_queues(queues, w_queue, destination, part)
                break

            condition, destination = rule.split(":")
            if "<" in rule:
                proprty, value = condition.split("<")
                if part[proprty] < int(value):
                    add_part_to_queues(queues, w_queue, destination, part)
                    break
            if ">" in rule:
                proprty, value = condition.split(">")
                if part[proprty] > int(value):
                    add_part_to_queues(queues, w_queue, destination, part)
                    break

    result = 0
    for part in queues["A"]:
        print(part)
        result += part["x"] + part["m"] + part["a"] + part["s"]
    print(result)



if __name__ == '__main__':
    data = read_data()
    print(solve(*data))
