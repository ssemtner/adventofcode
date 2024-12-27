import time
import unittest
from itertools import combinations

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def solve(path):
    with open(path) as file:
        grid = [list(line.strip()) for line in file.readlines()]

    n, m = len(grid), len(grid[0])
    start = (0, 0)
    end = (0, 0)
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "S":
                start = (i, j)
            if grid[i][j] == "E":
                end = (i, j)

    n, m = len(grid), len(grid[0])
    q: list[tuple[int, int]] = [(start[0], start[1])]
    dists: dict[tuple[int, int], int] = {start: 0}
    while q:
        i, j = q.pop(0)
        if (i, j) == end:
            break
        for di, dj in DIRS:
            ii, jj = i + di, j + dj
            if (
                0 <= ii < n
                and 0 <= jj < m
                and grid[ii][jj] != "#"
                and (ii, jj) not in dists
            ):
                q.append((ii, jj))
                dists[(ii, jj)] = dists[(i, j)] + 1

    p1, p2 = 0, 0

    for (a, i), (b, j) in combinations(dists.items(), 2):
        d = abs(a[0] - b[0]) + abs(a[1] - b[1])
        if d == 2 and j - i - d >= 100:
            p1 += 1
        if d <= 20 and j - i - d >= 100:
            p2 += 1

    return p1, p2


class TestDay(unittest.TestCase):
    def test(self):
        self.assertEqual(solve("../data/sample/day20.txt"), (0, 0))


if __name__ == "__main__":
    start = time.time()
    p1, p2 = solve("../data/day20.txt")
    elapsed = time.time() - start
    print(f"part 1: {p1} ({elapsed:.4f}s)")
    print(f"part 2: {p2} ({elapsed:.4f}s)")

    unittest.main()
