import time
from typing import List, Tuple
import unittest
import heapq as hq


def solve(path):
    with open(path) as file:
        grid = [list(line.strip()) for line in file]

    n, m = len(grid), len(grid[0])

    start = (0, 0)
    end = (0, 0)
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "S":
                start = (i, j)
            elif grid[i][j] == "E":
                end = (i, j)

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    dist = [[[10000000 for _ in range(4)] for _ in range(m)] for _ in range(n)]

    for i in range(4):
        dist[start[0]][start[1]][i] = 0

    pq: List[Tuple[int, int, int, int]] = [(0, start[0], start[1], 1)]
    seen = set()

    while pq:
        cur, x, y, d = hq.heappop(pq)
        if (x, y, d) in seen:
            continue
        seen.add((x, y, d))
        if cur < dist[x][y][d]:
            dist[x][y][d] = cur
        dx, dy = directions[d]
        xx, yy = x + dx, y + dy
        if xx in range(n) and yy in range(m) and grid[xx][yy] != "#":
            hq.heappush(pq, (cur + 1, xx, yy, d))
        hq.heappush(pq, (cur + 1000, x, y, (d + 1) % 4))
        hq.heappush(pq, (cur + 1000, x, y, (d + 3) % 4))

    best = min(dist[end[0]][end[1]])

    rdist = [[[10000000 for _ in range(4)] for _ in range(m)] for _ in range(n)]

    for i in range(4):
        rdist[end[0]][end[1]][i] = 0

    pq: List[Tuple[int, int, int, int]] = [(0, end[0], end[1], i) for i in range(4)]
    seen = set()

    while pq:
        cur, x, y, d = hq.heappop(pq)
        if (x, y, d) in seen:
            continue
        seen.add((x, y, d))
        if cur < rdist[x][y][d]:
            rdist[x][y][d] = cur
        dx, dy = directions[(d + 2) % 4]
        xx, yy = x + dx, y + dy
        if xx in range(n) and yy in range(m) and grid[xx][yy] != "#":
            hq.heappush(pq, (cur + 1, xx, yy, d))
        hq.heappush(pq, (cur + 1000, x, y, (d + 1) % 4))
        hq.heappush(pq, (cur + 1000, x, y, (d + 3) % 4))

    valid = set()
    for i in range(n):
        for j in range(m):
            for d in range(4):
                if dist[i][j][d] + rdist[i][j][d] == best:
                    valid.add((i, j))

    return (best, len(valid))


class TestDay(unittest.TestCase):
    def test(self):
        self.assertEqual(solve("../data/sample/day16.txt"), (11048, 64))


if __name__ == "__main__":
    start = time.time()
    p1, p2 = solve("../data/day16.txt")
    elapsed = time.time() - start
    print(f"part 1: {p1} ({elapsed:.4f}s)")
    print(f"part 2: {p2} ({elapsed:.4f}s)")

    unittest.main()
