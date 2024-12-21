import unittest


def solve(path, p2):
    with open(path) as file:
        grid = [[int(x) for x in line.strip()] for line in file]

    n, m = len(grid), len(grid[0])
    trailheads = [
        t
        for row in [[(i, j) for j in range(m) if grid[i][j] == 0] for i in range(n)]
        for t in row
    ]

    visited = set()

    def score(i, j, target, p2):
        if (
            i not in range(n)
            or j not in range(m)
            or (i, j) in visited
            or grid[i][j] != target
        ):
            return 0
        if not p2:
            visited.add((i, j))
        if target == 9:
            return 1
        if p2:
            visited.add((i, j))
        ways = sum(
            score(i + di, j + dj, target + 1, p2)
            for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0))
        )
        if p2:
            visited.remove((i, j))
        return ways

    return sum(score(t[0], t[1], 0, p2) for t in trailheads if visited.clear() is None)


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(solve("../data/sample/day10.txt", False), 36)

    def test_part2(self):
        self.assertEqual(solve("../data/sample/day10.txt", True), 81)


if __name__ == "__main__":
    import time

    start = time.time()
    print(f"part 1: {solve('../data/day10.txt', False)} ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: {solve('../data/day10.txt', True)} ({time.time() - start:.4f}s)")

    unittest.main()
