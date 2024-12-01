import unittest
from collections import defaultdict

def part1(path):
    l1 = []
    l2 = []
    with open(path, "r") as file:
        for line in file.readlines():
            if line == "":
                continue
            a = line.split("   ")
            l1.append(int(a[0]))
            l2.append(int(a[1]))

    l1 = sorted(l1)
    l2 = sorted(l2)
    sum = 0

    for a, b in zip(l1, l2):
        sum += abs(a - b)

    return sum


def part2(path):
    l1 = []
    l2 = []
    with open(path, "r") as file:
        for line in file.readlines():
            if line == "":
                continue
            a = line.split("   ")
            l1.append(int(a[0]))
            l2.append(int(a[1]))

    counts = defaultdict(int)
    for a in l2:
        counts[a] += 1

    sum = 0

    for a in l1:
        sum += counts[a] * a

    return sum


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day1.txt"), 11)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day1.txt"), 31)


if __name__ == "__main__":
    print("part 1:", part1("../data/day1.txt"))
    print("part 2:", part2("../data/day1.txt"))

    unittest.main()
