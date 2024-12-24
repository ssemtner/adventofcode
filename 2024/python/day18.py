import time
import unittest
import re

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def prepare(path):
    with open(path) as file:
        coords = [(int(x), int(y)) for x, y in re.findall(r"(\d+),(\d+)", file.read())]

    return coords


def part1(path, n, c):
    blocked = set(prepare(path)[:c])
    q: list[tuple[int, int, int]] = [(0, 0, 0)]
    while q:
        x, y, d = q.pop(0)
        if x == n and y == n:
            return d
        for dx, dy in DIRS:
            xx, yy = x + dx, y + dy
            if 0 <= xx <= n and 0 <= yy <= n and (xx, yy) not in blocked:
                blocked.add((xx, yy))
                q.append((xx, yy, d + 1))
    return -1


def part2(path, n):
    coords = prepare(path)
    blocked = set()

    def dfs():
        seen = set()

        s = [(0, 0)]
        while s:
            x, y = s.pop()

            if x == n and y == n:
                return True

            if (x, y) in seen:
                continue

            seen.add((x, y))

            for dx, dy in DIRS:
                xx, yy = x + dx, y + dy
                if 0 <= xx <= n and 0 <= yy <= n and (xx, yy) not in blocked:
                    s.append((xx, yy))
        return False

    # really slow (5s) but whatever
    for x, y in coords:
        blocked.add((x, y))
        if not dfs():
            return f"{x},{y}"


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day18.txt", 6, 12), 22)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day18.txt", 6), "6,1")


if __name__ == "__main__":
    start = time.time()
    print(
        f"part 1: {part1('../data/day18.txt', 70, 1024)} ({time.time() - start:.4f}s)"
    )

    start = time.time()
    print(f"part 2: \"{part2('../data/day18.txt', 70)}\" ({time.time() - start:.4f}s)")

    unittest.main()
