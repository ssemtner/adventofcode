import unittest
import math


def part1(path):
    games = []
    with open(path, "r") as file:
        lines = file.readlines()
        times = [int(x) for x in lines[0].split(":")[1].split()]
        distances = [int(x) for x in lines[1].split(":")[1].split()]
        games = list(zip(times, distances))

    score = 1
    for game in games:
        winning = 0
        for time in range(game[0]):
            distance = time * (game[0] - time)
            if distance > game[1]:
                winning += 1
        score *= winning

    return score


def part2(path):
    with open(path, "r") as file:
        # brute force bay way but it's not even that slow
        time = int(file.readline().split(":")[1][:-1].replace(" ", ""))
        distance = int(file.readline().split(":")[1][:-1].replace(" ", ""))

        # y = x * (time - x)
        # y = time * x - x^2
        # solve for y = distance, then take t - 2x as solution
        # 0 = time * x - x^2 - distance
        # quadratic formula
        # x = (-b +- sqrt(b^2 - 4ac)) / 2a
        # x = (-time +- sqrt(time^2 - 4 * -1 * -distance)) / 2
        # x = (-time +- sqrt(time^2 - 4 * distance)) / 2

        # This version is off by one sometimes
        # so I'm just going with brute force for now
        # x2 = -time + math.sqrt((time * time) - (4 * distance))
        # return round(time + x2)

        winning = 0
        for t in range(time):
            d = t * (time - t)
            if d > distance:
                winning += 1

        return winning


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day6.txt"), 288)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day6.txt"), 71503)


if __name__ == "__main__":
    import time

    p1start = time.time()
    print("part 1:", part1("../data/day6.txt"))
    p1end = time.time()
    p2start = time.time()
    print("part 2:", part2("../data/day6.txt"))
    p2end = time.time()
    print("part 1 time:", p1end - p1start)
    print("part 2 time:", p2end - p2start)

    unittest.main()
