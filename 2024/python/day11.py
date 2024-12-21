import unittest
import functools
from collections import defaultdict


@functools.cache
def blink(n):
    if n == 0:
        return [1]
    s = str(n)
    if len(s) % 2 == 0:
        m = len(s) // 2
        return [int(s[:m]), int(s[m:])]
    else:
        return [n * 2024]


def solve(path, n):
    with open(path) as file:
        stones = [int(x) for x in file.readline().strip().split()]

    counts = defaultdict(int)
    for s in stones:
        counts[s] += 1

    for _ in range(n):
        new = defaultdict(int)
        for s, c in counts.items():
            for x in blink(s):
                new[x] += c
        counts = new
    return sum(counts.values())


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(solve("../data/sample/day11.txt", 25), 55312)


if __name__ == "__main__":
    import time

    start = time.time()
    print(f"part 1: {solve('../data/day11.txt', 25)} ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: {solve('../data/day11.txt', 75)} ({time.time() - start:.4f}s)")

    unittest.main()
