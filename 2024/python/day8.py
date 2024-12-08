import unittest
from collections import defaultdict


def solve(path, p2=False):
    antennas = defaultdict(list)
    with open(path) as file:
        lines = file.readlines()
        n, m = len(lines), len(lines[0].strip())
        for i, line in enumerate(lines):
            for j, char in enumerate(line.strip()):
                if char != ".":
                    antennas[char].append((i, j))

    antinodes = set()

    def add(p, di, dj):
        i, j = p
        if not p2:
            i += di
            j += dj
        while i in range(n) and j in range(m):
            antinodes.add((i, j))
            if not p2:
                break
            i += di
            j += dj

    for _, values in antennas.items():
        for x in values:
            for y in values:
                if x == y:
                    continue
                di = x[0] - y[0]
                dj = x[1] - y[1]
                add(x, di, dj)
                add(y, -di, -dj)

    return len(antinodes)


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(solve("../data/sample/day8.txt"), 14)

    def test_part2(self):
        self.assertEqual(solve("../data/sample/day8.txt", p2=True), 34)


if __name__ == "__main__":
    print("part 1:", solve("../data/day8.txt"))
    print("part 2:", solve("../data/day8.txt", p2=True))

    unittest.main()
