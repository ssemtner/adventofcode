import unittest
import math


def part1(path):
    result = 0
    with open(path, "r") as file:
        for line in file.readlines():
            sequence = [int(x) for x in line.strip().split()]

            states = [sequence]
            idx = 0
            while any([x != 0 for x in states[idx]]):
                state = states[idx]
                idx += 1
                # calculate differences
                diffs = [0] * (len(state) - 1)
                for i in range(len(state) - 1):
                    diffs[i] = state[i + 1] - state[i]

                states.append(diffs)

            # start from bottom
            states[-1].append(0)

            # walk up
            for i in range(idx - 1, -1, -1):
                states[i].append(states[i + 1][-1] + states[i][-1])

            result += states[0][-1]
        return result


def part2(path):
    result = 0
    with open(path, "r") as file:
        for line in file.readlines():
            sequence = [int(x) for x in line.strip().split()]

            states = [sequence]
            idx = 0
            while any([x != 0 for x in states[idx]]):
                state = states[idx]
                idx += 1
                # calculate differences
                diffs = [0] * (len(state) - 1)
                for i in range(len(state) - 1):
                    diffs[i] = state[i + 1] - state[i]

                states.append(diffs)

            # start from bottom
            states[-1] = [0] + states[-1]

            # walk up
            for i in range(idx - 1, -1, -1):
                states[i] = [states[i][0] - states[i + 1][0]] + states[i]
                # print(states[i])

            # print(states)
            result += states[0][0]
            # print(states[0][0])
        return result


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day9.txt"), 114)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day9.txt"), 2)


if __name__ == "__main__":
    import time

    p1start = time.time()
    print("part 1:", part1("../data/day9.txt"))
    p1end = time.time()
    p2start = time.time()
    print("part 2:", part2("../data/day9.txt"))
    p2end = time.time()
    print("part 1 time:", p1end - p1start)
    print("part 2 time:", p2end - p2start)

    unittest.main()
