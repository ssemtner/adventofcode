from functools import reduce
import time
import unittest


def parse(path):
    with open(path) as file:
        return [
            [
                [int(x) for x in part.split("=")[1].split(",")]
                for part in line.split(" ")
            ]
            for line in file.readlines()
        ]


def position(n, m, sx, sy, vx, vy, t):
    return (sx + vx * t) % n, (sy + vy * t) % m


def part1(path, n, m):
    robots = parse(path)

    mn = n // 2
    mm = m // 2
    quadrants = [0 for _ in range(4)]

    for (sx, sy), (vx, vy) in robots:
        x, y = position(n, m, sx, sy, vx, vy, 100)

        if x < mn and y < mm:
            quadrants[0] += 1
        elif x > mn and y < mm:
            quadrants[1] += 1
        elif x < mn and y > mm:
            quadrants[2] += 1
        elif x > mn and y > mm:
            quadrants[3] += 1

    return reduce(lambda x, y: x * y, quadrants)


def part2(path, n, m):
    robots = parse(path)
    for i in range(10000):
        close = set()
        possible = set()
        for (sx, sy), (vx, vy) in robots:
            x, y = position(n, m, sx, sy, vx, vy, i)
            if (x, y) in possible:
                close.add((x, y))
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    possible.add((x + dx, y + dy))

        if len(close) > 200:
            print(f"t: {i}")
            for y in range(m):
                for x in range(n):
                    if (x, y) in close:
                        print("#", end="")
                    elif (x, y) in possible:
                        print(".", end="")
                    else:
                        print(" ", end="")
                print()
            return i


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day14.txt", 11, 7), 12)


if __name__ == "__main__":
    start = time.time()
    print(
        f"part 1: {part1('../data/day14.txt', 101, 103)} ({time.time() - start:.4f}s)"
    )

    start = time.time()
    print(
        f"part 2: {part2('../data/day14.txt', 101, 103)} ({time.time() - start:.4f}s)"
    )

    unittest.main()
