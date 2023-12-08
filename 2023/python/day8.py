import unittest
import math


def part1(path):
    nodes = {}
    pattern = []

    with open(path, "r") as file:
        lines = file.readlines()
        pattern = list(lines[0].strip())

        for line in lines[1:]:
            nodes[line[0:3]] = (line[0:3], line[7:10], line[12:15])

    i = 0
    cur = nodes["AAA"]
    while cur[0] != "ZZZ":
        match pattern[i % len(pattern)]:
            case "L":
                cur = nodes[cur[1]]
            case "R":
                cur = nodes[cur[2]]

        i += 1

    return i


def part2(path):
    nodes = {}
    pattern = []
    with open(path, "r") as file:
        lines = file.readlines()
        pattern = list(lines[0].strip())

        for line in lines[1:]:
            nodes[line[0:3]] = (line[0:3], line[7:10], line[12:15])

    steps = 0
    paths = [node for node in nodes.values() if node[0][-1] == "A"]
    step_counts = []
    while len(paths) > 0:
        match pattern[steps % len(pattern)]:
            case "L":
                paths = [nodes[x[1]] for x in paths]
            case "R":
                paths = [nodes[x[2]] for x in paths]

        for i, path in enumerate(paths):
            if path[0][-1] == "Z":
                step_counts.append(steps + 1)
                paths.pop(i)

        steps += 1

    # had to cheat for this lmao
    # no chance I would have figured it out
    return math.lcm(*step_counts)


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day8sample1.txt"), 2)
        self.assertEqual(part1("../data/sample/day8sample2.txt"), 6)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day8sample3.txt"), 6)


if __name__ == "__main__":
    import time

    p1start = time.time()
    print("part 1:", part1("../data/day8.txt"))
    p1end = time.time()
    p2start = time.time()
    print("part 2:", part2("../data/day8.txt"))
    p2end = time.time()
    print("part 1 time:", p1end - p1start)
    print("part 2 time:", p2end - p2start)

    unittest.main()
