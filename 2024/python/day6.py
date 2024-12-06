import unittest
import tqdm

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def part1(path):
    grid = []
    with open(path) as file:
        grid = [list(line.strip()) for line in file.readlines()]

    i, j = start(grid)
    count, _ = solve(i, j, grid)

    return len(count)


def part2(path):
    grid = []
    with open(path) as file:
        grid = [list(line.strip()) for line in file.readlines()]

    i, j = start(grid)

    # slight pruning by avoiding anything that could not touch the path
    s, _ = solve(i, j, grid)

    def worth(x, y):
        for dx in [0, 1, -1]:
            for dy in [0, 1, -1]:
                if (x + dx, y + dy) in s:
                    return True
        return False

    count = 0

    # bad and brute force but I'll fix it once I rewrite everything in another language
    for x in tqdm.tqdm(range(len(grid))):
        for y in range(len(grid[i])):
            if not worth(x, y):
                continue
            if grid[x][y] == ".":
                grid[x][y] = "#"
                _, loop = solve(i, j, grid)
                if loop:
                    count += 1
                grid[x][y] = "."
    return count


def solve(i, j, grid):
    n = len(grid)
    m = len(grid[0])
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    d = 0

    visited = set()
    count = set()

    while True:
        if (i, j, d) in visited:
            return None, True
        visited.add((i, j, d))
        count.add((i, j))
        i_next, j_next = i + dirs[d][0], j + dirs[d][1]
        if i_next not in range(n) or j_next not in range(m):
            break
        if grid[i_next][j_next] == "#":
            d = (d + 1) % 4
        else:
            i, j = i_next, j_next
    return count, False


def start(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "^":
                return x, y


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day6.txt"), 41)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day6.txt"), 6)


if __name__ == "__main__":
    print("part 1:", part1("../data/day6.txt"))
    print("part 2:", part2("../data/day6.txt"))

    unittest.main()
