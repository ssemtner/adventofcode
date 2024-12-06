import unittest


def part1(path):
    count = 0
    grid = []
    with open(path) as file:
        grid = [list(line.strip()) for line in file.readlines()]

    n = len(grid)
    m = len(grid[0])

    chars = "XMAS"

    def dfs(i, j, c, di, dj):
        if i not in range(n) or j not in range(m) or grid[i][j] != chars[c]:
            return False
        if c == len(chars) - 1:
            return True
        if dfs(i + di, j + dj, c + 1, di, dj):
            return True
        return False

    for i in range(n):
        for j in range(m):
            if grid[i][j] == "X":
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if dfs(i, j, 0, di, dj):
                            count += 1

    return count


def part2(path):
    count = 0
    grid = []
    with open(path) as file:
        grid = [list(line.strip()) for line in file.readlines()]

    n = len(grid)
    m = len(grid[0])

    def eq(i, j, c):
        return i in range(n) and j in range(m) and grid[i][j] == c

    for i in range(n):
        for j in range(m):
            if grid[i][j] == "A":
                if (eq(i - 1, j - 1, "M") and eq(i + 1, j + 1, "S")) or (
                    eq(i - 1, j - 1, "S") and eq(i + 1, j + 1, "M")
                ):
                    if (eq(i - 1, j + 1, "M") and eq(i + 1, j - 1, "S")) or (
                        eq(i - 1, j + 1, "S") and eq(i + 1, j - 1, "M")
                    ):
                        count += 1
    return count


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day4.txt"), 18)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day4.txt"), 9)


if __name__ == "__main__":
    print("part 1:", part1("../data/day4.txt"))
    print("part 2:", part2("../data/day4.txt"))

    unittest.main()
