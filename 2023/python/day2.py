import unittest
from typing import Dict, List


def parse_game(line: str) -> (int, List[Dict[str, int]]):
    number = int(line.split(": ")[0].split(" ")[1])
    draw_strs = line.split(": ")[1].split("; ")
    draws = []
    for draw_str in draw_strs:
        colors = [draw.split(" ") for draw in draw_str.split(", ")]
        draws.append({color[1]: int(color[0]) for color in colors})

    return number, draws


def part1(path):
    with open(path, "r") as file:
        sum = 0
        for line in file.readlines():
            number, draws = parse_game(line.strip())
            limits = {"red": 12, "green": 13, "blue": 14}
            for draw in draws:
                for color, quantity in draw.items():
                    if color in limits:
                        if quantity > limits[color]:
                            break
                else:
                    continue
                break
            else:
                sum += number

        return sum


def part2(path):
    with open(path, "r") as file:
        sum = 0
        for line in file.readlines():
            _, draws = parse_game(line.strip())
            maximums = {}
            for draw in draws:
                for color, quantity in draw.items():
                    if color in maximums:
                        maximums[color] = max(maximums[color], quantity)
                    else:
                        maximums[color] = quantity
            power = 1
            for maximum in maximums.values():
                power *= maximum
            sum += power

        return sum


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day2.txt"), 8)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day2.txt"), 2286)


if __name__ == "__main__":
    print("part 1:", part1("../data/day2.txt"))
    print("part 2:", part2("../data/day2.txt"))

    unittest.main()
