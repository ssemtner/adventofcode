import unittest
from typing import List


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y


class NumBounds:
    def __init__(self, left: Point, right: Point):
        assert left.y == right.y

        self.left = left
        self.right = right

    def __repr__(self):
        return f"[{self.left}, {self.right}]"

    def adjacent_points(self) -> List[Point]:
        points = []
        for x in range(self.left.x - 1, self.right.x + 2):
            for y in range(self.left.y - 1, self.left.y + 2):
                points.append(Point(x, y))

        return points

    def adjacent(self, p: Point):
        # print(self, p)
        return (
            self.left.y - 1 <= p.y <= self.left.y + 1
            and self.left.x - 1 <= p.x <= self.right.x + 1
        )


def part1(path):
    symbols = []
    numbers = []
    with open(path, "r") as file:
        for row, line in enumerate(file.readlines()):
            num_str = ""
            num_left = None
            for col, char in enumerate(line.strip()):
                if char in ["@", "#", "$", "%", "&", "*", "/", "+", "=", "-"]:
                    symbols.append(Point(col, row))

                    if num_str != "":
                        num = int(num_str)
                        num_str = ""
                        numbers.append((num, NumBounds(num_left, Point(col - 1, row))))
                elif char != ".":
                    if num_str == "":
                        num_left = Point(col, row)
                    num_str += char
                else:
                    if num_str != "":
                        num = int(num_str)
                        num_str = ""
                        numbers.append((num, NumBounds(num_left, Point(col - 1, row))))
            if num_str != "":
                num = int(num_str)
                num_str = ""
                numbers.append((num, NumBounds(num_left, Point(col - 1, row))))
        # print(numbers)
        sum = 0
        for num, bounds in numbers:
            valid_points = bounds.adjacent_points()
            for symbol in symbols:
                if symbol in valid_points:
                    sum += num
                    break

        return sum


def part2(path):
    symbols = []
    numbers = []
    with open(path, "r") as file:
        for row, line in enumerate(file.readlines()):
            num_str = ""
            num_left = None
            for col, char in enumerate(line.strip()):
                if char == "*":
                    symbols.append(Point(col, row))

                    if num_str != "":
                        num = int(num_str)
                        num_str = ""
                        numbers.append((num, NumBounds(num_left, Point(col - 1, row))))
                elif char.isdigit():
                    if num_str == "":
                        num_left = Point(col, row)
                    num_str += char
                else:
                    if num_str != "":
                        num = int(num_str)
                        num_str = ""
                        numbers.append((num, NumBounds(num_left, Point(col - 1, row))))
            if num_str != "":
                num = int(num_str)
                num_str = ""
                numbers.append((num, NumBounds(num_left, Point(col - 1, row))))

        sum = 0
        for symbol in symbols:
            matches = []
            for num, bounds in numbers:
                if bounds.adjacent(symbol):
                    matches.append(num)
            if len(matches) == 2:
                sum += matches[0] * matches[1]

        return sum


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day3.txt"), 4361)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day3.txt"), 467835)


if __name__ == "__main__":
    print("part 1:", part1("../data/day3.txt"))
    print("part 2:", part2("../data/day3.txt"))

    unittest.main()
