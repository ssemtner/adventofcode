from itertools import product
import time
import unittest


def part1(path):
    locks: list[list[int]] = []
    keys: list[list[int]] = []
    with open(path) as file:
        for text in file.read().strip().split("\n\n"):
            lines = text.splitlines()

            cols = [sum(1 for c in col if c == "#") for col in zip(*lines[1:-1])]

            if all(c == "#" for c in lines[0]) and all(c == "." for c in lines[-1]):
                locks.append(cols)
            else:
                keys.append(cols)

    return sum(
        all(l + k <= 5 for l, k in zip(lock, key)) for lock, key in product(locks, keys)
    )


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day25.txt"), 3)


if __name__ == "__main__":
    start = time.time()
    print(f"part 1: {part1('../data/day25.txt')} ({time.time() - start:.4f}s)")

    unittest.main()
