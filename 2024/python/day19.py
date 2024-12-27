import time
import unittest


# lots of duplicated code and pretty sure I can use a trie to speed this up


def part1(path):
    with open(path) as file:
        lines = file.readlines()
        patterns = lines[0].strip().split(", ")

    res = 0
    for target in [line.strip() for line in lines[2:]]:
        dp = [0 for _ in range(len(target) + 1)]
        dp[0] = 1
        for i in range(1, len(target) + 1):
            for pattern in patterns:
                if target[i - len(pattern) : i] == pattern:
                    dp[i] += dp[i - len(pattern)]
        res += dp[-1] > 0
    return res


def part2(path):
    with open(path) as file:
        lines = file.readlines()
        patterns = lines[0].strip().split(", ")

    res = 0
    for target in [line.strip() for line in lines[2:]]:
        dp = [0 for _ in range(len(target) + 1)]
        dp[0] = 1
        for i in range(1, len(target) + 1):
            for pattern in patterns:
                if target[i - len(pattern) : i] == pattern:
                    dp[i] += dp[i - len(pattern)]
        res += dp[-1]
    return res


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day19.txt"), 6)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day19.txt"), 16)


if __name__ == "__main__":
    start = time.time()
    print(f"part 1: {part1('../data/day19.txt')} ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: {part2('../data/day19.txt')} ({time.time() - start:.4f}s)")

    unittest.main()
