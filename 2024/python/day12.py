import unittest

from collections import defaultdict


def part1(path):
    grid = []
    with open(path) as file:
        for line in file.readlines():
            grid.append([x for x in line.strip()])

    n, m = len(grid), len(grid[0])

    visited = set()

    def expand(i, j, plant):
        if i not in range(n) or j not in range(m) or grid[i][j] != plant:
            return 0, 1
        if (i, j) in visited:
            return 0, 0
        visited.add((i, j))
        area, perim = 1, 0
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            a, p = expand(i + di, j + dj, plant)
            area += a
            perim += p
        return area, perim

    res = 0
    for i in range(n):
        for j in range(m):
            if (i, j) in visited:
                continue
            area, perim = expand(i, j, grid[i][j])
            res += area * perim

    return res


def part2(path):
    grid = []
    with open(path) as file:
        for line in file.readlines():
            grid.append([x for x in line.strip()])

    n, m = len(grid), len(grid[0])

    visited = set()
    outgoing = defaultdict(set)

    def expand(i, j, plant, direction):
        if i not in range(n) or j not in range(m) or grid[i][j] != plant:
            if direction is not None:
                outgoing[direction].add((i, j))
            return 0, 1
        if (i, j) in visited:
            return 0, 0
        visited.add((i, j))
        area, perim = 1, 0
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            a, p = expand(i + di, j + dj, plant, (di, dj))
            area += a
            perim += p
        return area, perim

    def sides(outgoing):
        num = 0
        for _, positions in outgoing.items():
            seen = set()
            for i, j in positions:
                if (i, j) in seen:
                    continue
                num += 1
                q = [(i, j)]
                while q:
                    i, j = q.pop()
                    if (i, j) in seen or (i, j) not in positions:
                        continue
                    seen.add((i, j))
                    for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        q.append((i + di, j + dj))
        return num

    res = 0
    for i in range(n):
        for j in range(m):
            if (i, j) in visited:
                continue
            outgoing.clear()
            area, _ = expand(i, j, grid[i][j], None)
            res += area * sides(outgoing)

    return res


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day12.txt"), 1930)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day12.txt"), 1206)


if __name__ == "__main__":
    import time

    start = time.time()
    print(f"part 1: {part1('../data/day12.txt')} ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: {part2('../data/day12.txt')} ({time.time() - start:.4f}s)")

    unittest.main()
