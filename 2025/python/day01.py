import unittest


def part1(path):
    val = 50
    res = 0
    with open(path, "r") as file:
        for line in file.readlines():
            i = int(line[1:])
            if line[0] == "L":
                i = -i
            val += i
            val = val % 100
            if val == 0:
                res += 1
    return res


def part2(path):
    val = 50
    res = 0
    with open(path, "r") as file:
        for line in file.readlines():
            i = int(line[1:])
            if line[0] == "L":
                i = -i
            val += i
            res += abs(val // 100)
            val = val % 100
    return res


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day01.txt"), 3)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day01.txt"), 6)


if __name__ == "__main__":
    print("part 1:", part1("../data/day01.txt"))
    print("part 2:", part2("../data/day01.txt"))

    unittest.main()
