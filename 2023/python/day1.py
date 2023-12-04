from optparse import OptionParser
import unittest

def part1(path):
    sum = 0
    with open(path, "r") as file:
        for line in file.readlines():
            for c in line:
                try:
                    v = int(c)
                    sum += v * 10
                    break
                except ValueError:
                    continue
            for c in line[::-1]:
                try:
                    v = int(c)
                    sum += v
                    break
                except ValueError:
                    continue
    return sum


def part2(path):
    sum = 0

    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
             "six": 6, "seven": 7, "eight": 8, "nine": 9}

    with open(path, "r") as file:
        for line in file.readlines():
            line = line.strip()
            s = ""
            for c in line:
                try:
                    v = int(c)
                    sum += v * 10
                    break
                except ValueError:
                    s += c
                    for (word, value) in words.items():
                        if word in s:
                            sum += value * 10
                            s = ""
                            break
                    else:
                        continue
                    break
            
            s = ""
            for c in line[::-1]:
                try:
                    v = int(c)
                    sum += v
                    break
                except ValueError:
                    s = c + s
                    for (word, value) in words.items():
                        if word in s:
                            sum += value
                            s = ""
                            break
                    else:
                        continue
                    break
    return sum


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day1part1.txt"), 142)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day1part2.txt"), 281)


if __name__ == "__main__":
    print("part 1:", part1("../data/day1.txt"))
    print("part 2:", part2("../data/day1.txt"))

    unittest.main()
    
