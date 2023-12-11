import unittest


def solve(path, mult):
    grid = []
    with open(path, "r") as file:
        for line in file.readlines():
            grid.append([x for x in line.strip()])

    expanded_rows = [all([x == "." for x in grid[i]]) for i in range(len(grid))]
    expanded_cols = [
        all([x == "." for x in [row[i] for row in grid]]) for i in range(len(grid[0]))
    ]

    stars = []

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "#":
                stars.append((i, j))

    res = 0
    pairs = set()

    for star1 in stars:
        x1 = star1[1]
        y1 = star1[0]
        for star2 in stars:
            if star1 == star2:
                continue
            if (star2, star1) in pairs:
                continue

            pairs.add((star1, star2))

            res += sum(
                [
                    mult if expanded_cols[i] else 1
                    for i in range(min(x1, star2[1]), max(x1, star2[1]))
                ]
            ) + sum(
                [
                    mult if expanded_rows[i] else 1
                    for i in range(min(y1, star2[0]), max(y1, star2[0]))
                ]
            )

    return res


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(solve("../data/sample/day11.txt", 2), 374)

    def test_part2(self):
        self.assertEqual(solve("../data/sample/day11.txt", 10), 1030)
        self.assertEqual(solve("../data/sample/day11.txt", 100), 8410)


if __name__ == "__main__":
    import time

    p1start = time.time()
    print("part 1:", solve("../data/day11.txt", 2))
    p1end = time.time()
    p2start = time.time()
    print("part 2:", solve("../data/day11.txt", 1000000))
    p2end = time.time()
    print("part 1 time:", p1end - p1start)
    print("part 2 time:", p2end - p2start)

    unittest.main()
