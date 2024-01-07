import copy
import itertools
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


def read_data_pt2():
    pt1 = False
    f = open("19-full.in", "r")
    f = open("19.in", "r")
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
            new_instuctions = []
            for i in instructions:
                if ":" in i:
                    condition, result = i.split(":")
                    new_instuctions.append([condition, result])
                else:
                    new_instuctions.append([True, i])
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


def is_tree(workflows, queues, parts):
    parents = {}
    for workflow in workflows:
        rules = workflows[workflow]
        for rule in rules:
            if ":" not in rule:
                destination = rule
            else:
                _, destination = rule.split(":")

            if destination == "A" or destination == "R":
                continue

            append_in_dict(parents, destination, workflow)
    for p in parents:
        if len(parents[p]) > 1:
            print(p)
    print(parents)


def transform_worflows(workflows):
    new_wf = {}
    counter = 0

    while len(workflows) > 0:
        wf = list(workflows.keys())[0]
        rules = workflows.pop(wf)
        # rules = workflows[wf]
        if len(rules) == 2:
            condition, destination = rules[0].split(":")
            new_wf[wf] = [condition, destination, rules[1]]
        else:
            condition, destination = rules[0].split(":")
            new_name = str(counter)
            counter += 1

            new_rule = [condition, destination, new_name]
            new_wf[wf] = new_rule
            workflows[new_name] = rules[1:]

    parents = {}
    for parent, rules in new_wf.items():
        append_in_dict(parents, rules[1], parent)
        append_in_dict(parents, rules[2], parent)

    return new_wf, parents


def apply_condition_to_ranges(condition, all_ranges, inverted=False):
    mapping = {"x": 0, "m":1, "a":2, "s":3}
    m = mapping[condition[0]]
    operator = condition[1]
    value = int(condition[2:])

    if inverted:
        if operator == ">":
            operator = "<"
            value = value
        else:
            operator = ">"
            value = value
    else:
        if operator == ">":
            value += 1
        else:
            value -= 1

    n_ranges = len(all_ranges)
    new_ranges = copy.deepcopy(all_ranges)

    for i in range(n_ranges):
        r = all_ranges[i]
        ranges = r[m]

        if len(ranges) == 0:
            continue

        new_range = []
        for w in ranges:
            if operator == ">":
                if value > w[1]:
                    continue
                if value > w[0]:
                    new_range.append([value, w[1]])
                    continue
                new_range.append(w)
            else:
                if value < w[0]:
                    continue
                if value < w[1]:
                    new_range.append([w[0], value])
                    continue
                new_range.append(w)
        new_ranges[i][m] = new_range
    return new_ranges


def add_range_to_list(ranges, r):
    if r is None:
        return ranges
    return ranges + [r]


def merge_ranges(r1, r2):
    new_range = []
    for r in itertools.chain(r1, r2):
        if r == [[], [], [], []]:
            continue
        new_range.append(r)
    return new_range


def solve_pt2(workflows, queues, parts):
    tree, parents = transform_worflows(workflows)
    tails = {"A": [[[[1, 4000]], [[1, 4000]], [[1, 4000]], [[1, 4000]]]], "R": [[[], [], [], []]]}
    queue = ["A", "R"]

    while True:
        if len(queue) == 0:
            break
        node_name = queue.pop(0)

        if node_name == "in":
            continue

        come_back_to_this_parent = False

        for parent in parents[node_name]:
            if parent in tails.keys():
                continue

            condition, left_child_name, right_child_name = tree[parent]
            if left_child_name not in tails.keys() or right_child_name not in tails.keys():
                come_back_to_this_parent = True
                continue

            if parent == "qqz":
                k = 3

            left_child = copy.deepcopy(tails[left_child_name])
            right_child = copy.deepcopy(tails[right_child_name])

            new_ranges_left = apply_condition_to_ranges(condition, left_child)
            new_ranges_right = apply_condition_to_ranges(condition, right_child, inverted=True)

            this_parent_range = merge_ranges(new_ranges_left, new_ranges_right)
            tails[parent] = this_parent_range
            queue.append(parent)

        if come_back_to_this_parent:
            queue.append(node_name)

    # rfg = count_possibilities(tails["rfg"])
    # rfg_ = 135234560000000
    # rn = count_possibilities(tails["crn"])
    # crn_ = 85632000000000
    # lnx = count_possibilities(tails["lnx"])
    # lnx_ = 256000000000000
    # pv = count_possibilities(tails["pv"])
    # pv_ = 109824000000000
    in_ = count_possibilities(tails["in"])
    in__ = 167409079868000
    # print(rfg, rfg_)
    # print(crn, crn_)
    # print(lnx, lnx_)
    # print(pv, pv_)
    print(in_, in__)
    return


def count_possibilities(all_ranges):
    result = 0
    for r in all_ranges:
        value = 1
        for attribute_list in r:
            k = count_possibilities_attribute(attribute_list)
            value = value * k
        # print(value)
        result += value

    # print("---")
    # print(result)
    return result


def count_possibilities_attribute(ranges):
    if len(ranges) == 0:
        return 0
    result = 0
    for fr, to in ranges:
        dif = to - fr + 1
        result += dif
    return result


if __name__ == '__main__':
    data = read_data()
    print(solve_pt2(*data))
