import unittest


def part1(path):
    ranges = []
    with open(path, "r") as file:
        ranges = [
            [int(r.split("-")[0]), int(r.split("-")[1])] for r in file.read().split(",")
        ]
    res = 0

    # brute force bc why not
    def valid(id: int):
        s = str(id)
        n = len(s)
        if n & 1 == 1:
            return True
        m = n // 2
        return s[:m] != s[m:]

    for start, end in ranges:
        for id in range(start, end + 1):
            if not valid(id):
                # print(id)
                res += id
    return res


def part2(path):
    ranges = []
    with open(path, "r") as file:
        ranges = [
            [int(r.split("-")[0]), int(r.split("-")[1])] for r in file.read().split(",")
        ]
    res = 0

    def valid(id: int):
        s = str(id)
        return s not in (s + s)[1:-1]

    for start, end in ranges:
        for id in range(start, end + 1):
            if not valid(id):
                res += id
    return res


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day02.txt"), 1227775554)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day02.txt"), 4174379265)


if __name__ == "__main__":
    print("part 1:", part1("../data/day02.txt"))
    print("part 2:", part2("../data/day02.txt"))

    unittest.main()
