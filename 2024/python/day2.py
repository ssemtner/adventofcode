import unittest


def safe(levels: list[int]) -> bool:
    last = levels[0]
    inc = levels[1] > last
    for i, level in enumerate(levels[1:]):
        if (
            (abs(level - last) not in range(1, 4))
            or (inc and level <= last)
            or (not inc and level >= last)
        ):
            return False

        last = level

    return True


def part1(path):
    res = 0
    with open(path) as file:
        for line in file.readlines():
            levels = [int(x) for x in line.split()]
            if safe(levels):
                res += 1
    return res


def part2(path):
    res = 0
    with open(path) as file:
        for line in file.readlines():
            levels = [int(x) for x in line.split()]
            if safe(levels):
                res += 1
                continue
            for i in range(len(levels)):
                changed = levels.copy()
                changed.pop(i)
                if safe(changed):
                    res += 1
                    break
    return res


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day2.txt"), 2)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day2.txt"), 4)


if __name__ == "__main__":
    print("part 1:", part1("../data/day2.txt"))
    print("part 2:", part2("../data/day2.txt"))

    unittest.main()
