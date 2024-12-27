from collections import defaultdict
import time
import unittest
from itertools import pairwise


def step(n: int):
    n = (n ^ (n * 64)) % 16777216
    n = (n ^ (n // 32)) % 16777216
    n = (n ^ (n * 2048)) % 16777216
    return n


def part1(path):
    res = 0
    with open(path) as file:
        for line in file.readlines():
            n = int(line)
            for _ in range(2000):
                n = step(n)
            res += n
    return res


def part2(path):
    with open(path) as file:
        gain = defaultdict(int)
        for line in file.readlines():
            n = int(line)
            nums = [n] + [n := step(n) for _ in range(2000)]
            diffs = [b % 10 - a % 10 for a, b in pairwise(nums)]
            seen = set()
            for i in range(len(nums) - 4):
                pattern = tuple(diffs[i : i + 4])
                if pattern not in seen:
                    seen.add(pattern)
                    gain[pattern] += nums[i + 4] % 10

        return max(gain.values())


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day22part1.txt"), 37327623)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day22part2.txt"), 23)


if __name__ == "__main__":
    start = time.time()
    print(f"part 1: {part1('../data/day22.txt')} ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: {part2('../data/day22.txt')} ({time.time() - start:.4f}s)")

    unittest.main()
