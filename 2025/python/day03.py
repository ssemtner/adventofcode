import unittest


def part1(path: str):
    res = 0
    with open(path, "r") as file:
        for line in file.readlines():
            vals = [int(x) for x in line.strip()]
            tens = max(vals[:-1])
            i = vals.index(tens)
            ones = max(vals[i + 1 :])
            res += tens * 10 + ones

    return res


def part2(path: str):
    res = 0
    with open(path, "r") as file:
        for line in file.readlines():
            joltage = 0
            start = 0
            vals = [int(x) for x in line.strip()]
            for i in range(12):
                # pick largest val leaving enough at end
                next = max(vals[start:] if i == 11 else vals[start : i - 11])
                start = vals[start:].index(next) + 1 + start
                joltage = joltage * 10 + next
            res += joltage

    return res


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day3.txt"), 357)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day3.txt"), 3121910778619)


if __name__ == "__main__":
    print("part 1:", part1("../data/day3.txt"))
    print("part 2:", part2("../data/day3.txt"))

    _ = unittest.main()
