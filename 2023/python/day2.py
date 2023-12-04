from optparse import OptionParser
import unittest

def part1(path):
    with open(path, "r") as file:
        pass


def part2(path):
    pass


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day1part1.txt"), 142)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day1part2.txt"), 281)


if __name__ == "__main__":
    print("part 1:", part1("../data/day1.txt"))
    print("part 2:", part2("../data/day1.txt"))

    unittest.main()
    
