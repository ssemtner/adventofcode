import unittest


def solvable(target, nums, total=0, i=0, p2=False):
    if i == len(nums):
        return total == target
    product = total * nums[i]
    sum_ = total + nums[i]
    concat = int(f"{total}{nums[i]}")

    return (
        solvable(target, nums, sum_, i + 1, p2)
        or (product <= target and solvable(target, nums, product, i + 1, p2))
        or (p2 and concat <= target and solvable(target, nums, concat, i + 1, p2))
    )


def parse(path):
    with open(path) as file:
        for line in file.readlines():
            target, nums = line.split(": ")
            target = int(target)
            nums = [int(x) for x in nums.split()]
            yield target, nums


def part1(path):
    return sum(
        target for target, nums in parse(path) if solvable(target, nums, p2=False)
    )


def part2(path):
    return sum(
        target for target, nums in parse(path) if solvable(target, nums, p2=True)
    )


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day7.txt"), 3749)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day7.txt"), 11387)


if __name__ == "__main__":
    print("part 1:", part1("../data/day7.txt"))
    print("part 2:", part2("../data/day7.txt"))

    unittest.main()
