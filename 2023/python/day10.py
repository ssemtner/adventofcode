import unittest
import math
import numpy as np
from matplotlib.path import Path


types = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
}


def part1(path):
    grid = []
    with open(path, "r") as file:
        for line in file.readlines():
            grid.append([x for x in line.strip()])

    # find S
    s = (0, 0)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                s = (i, j)

    i = s[0] + 1
    j = s[1]
    last_step = (0, 0)
    traveled = 0
    while (i, j) != s or traveled == 0:
        for side in types[grid[i][j]]:
            if side == last_step:
                continue
            ii = i + side[0]
            jj = j + side[1]
            # print(side, i, j, grid[i][j], ii, jj, grid[ii][jj])
            try:
                traveled += 1
                i = ii
                j = jj
                last_step = (-side[0], -side[1])
                break

            except IndexError:
                pass

    return math.ceil(traveled / 2)


def part2(path):
    grid = []
    with open(path, "r") as file:
        for line in file.readlines():
            grid.append([x for x in line.strip()])

    # find S
    s = (0, 0)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                s = (i, j)

    i = s[0]
    j = s[1]
    last_step = (0, 0)
    parts = [s]

    # find first step
    for side in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        ii = i + side[0]
        jj = j + side[1]

        if ii < 0 or jj < 0 or ii >= len(grid) or jj >= len(grid[1]):
            continue

        thing = grid[ii][jj]

        if thing in types.keys():
            d = types[thing]
            if (-side[0], -side[1]) in d:
                i = ii
                j = jj
                last_step = (side[1], side[0])
                if grid[i][j] in ["L", "J", "F", "7"]:
                    parts.append((i, j))
                break

    position = [j, i]
    parts = [[s[1], s[0]], position]
    last_move = last_step
    while grid[position[1]][position[0]] != "S":
        parts.append([position[0], position[1]])
        tile = grid[position[1]][position[0]]
        if tile == "|":
            if last_move == [0, 1]:
                position[1] += 1
            elif last_move == [0, -1]:
                position[1] -= 1
        elif tile == "-":
            if last_move == [1, 0]:
                position[0] += 1
            elif last_move == [-1, 0]:
                position[0] -= 1
        elif tile == "7":
            if last_move == [1, 0]:
                position[1] += 1
                last_move = [0, 1]
            elif last_move == [0, -1]:
                position[0] -= 1
                last_move = [-1, 0]
        elif tile == "J":
            if last_move == [1, 0]:
                position[1] -= 1
                last_move = [0, -1]
            elif last_move == [0, 1]:
                position[0] -= 1
                last_move = [-1, 0]
        elif tile == "L":
            if last_move == [-1, 0]:
                position[1] -= 1
                last_move = [0, -1]
            elif last_move == [0, 1]:
                position[0] += 1
                last_move = [1, 0]
        elif tile == "F":
            if last_move == [-1, 0]:
                position[1] += 1
                last_move = [0, 1]
            elif last_move == [0, -1]:
                position[0] += 1
                last_move = [1, 0]
        else:
            print("ERROR")
            break

    # traveled = 0
    # while (i, j) != s:
    #     for side in types[grid[i][j]]:
    #         if side == last_step:
    #             continue
    #         ii = i + side[0]
    #         jj = j + side[1]
    #         # print(side, i, j, grid[i][j], ii, jj, grid[ii][jj])
    #         try:
    #             i = ii
    #             j = jj
    #             last_step = (-side[0], -side[1])
    #             traveled += 1
    #             if grid[i][j] in ["L", "J", "F", "7"]:
    #                 parts.append((i, j))
    #             break

    #         except IndexError:
    #             pass

    # parts.append(s)

    res = 0
    # p = Path(parts)
    # for y in range(len(grid)):
    #     for x in range(len(grid[i])):
    #         if [x, y] in parts:
    #             continue
    #         if p.contains_point((x, y)):
    #             res += 1

    # import matplotlib.pyplot as plt

    # plt.plot([x[0] for x in parts], [x[1] for x in parts])
    # print(len(parts))
    # plt.show()

    return res


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day10.txt"), 8)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day10part2.txt"), 10)


if __name__ == "__main__":
    import time

    # p1start = time.time()
    # print("part 1:", part1("../data/day10.txt"))
    # p1end = time.time()
    # p2start = time.time()
    # print("part 2:", part2("../data/day10.txt"))
    # p2end = time.time()
    # print("part 1 time:", p1end - p1start)
    # # print("part 2 time:", p2end - p2start)

    unittest.main()
