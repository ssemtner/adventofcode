import unittest
import re


def part1(path):
    res = 0
    with open(path) as file:
        for match in re.findall(r"mul\(([0-9]+),([0-9]+)\)", file.read()):
            res += int(match[0]) * int(match[1])
    return res


def part2(path):
    res = 0
    enabled = True
    with open(path) as file:
        for match in re.findall(
            r"mul\(([0-9]+),([0-9]+)\)|(do)\(\)|(don't)\(\)", file.read()
        ):
            if match[2]:
                enabled = True
            elif match[3]:
                enabled = False
            elif enabled:
                res += int(match[0]) * int(match[1])
    return res


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day3part1.txt"), 161)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day3part2.txt"), 48)


if __name__ == "__main__":
    print("part 1:", part1("../data/day3.txt"))
    print("part 2:", part2("../data/day3.txt"))

    unittest.main()
