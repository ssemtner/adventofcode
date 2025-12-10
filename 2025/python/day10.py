import unittest
import z3


# idk how to use z3 in rust so here


def part2(path: str):
    res = 0
    with open(path, "r") as file:
        for line in file.readlines():
            parts = line.split()
            # lights = parts[0]
            buttons = [
                [int(x) for x in button[1:-1].split(",")] for button in parts[1:-1]
            ]
            joltages = [int(x) for x in parts[-1][1:-1].split(",")]
            s = z3.Optimize()
            push_count = [z3.Int(f"push{i}") for i in range(len(buttons))]
            for i in range(len(buttons)):
                s.add(push_count[i] >= 0)
            for i in range(len(joltages)):
                # sum of buttons with this idx == value
                s.add(
                    sum(push_count[j] for j, btn in enumerate(buttons) if i in btn)
                    == joltages[i]
                )

            s.minimize(sum(push_count))
            assert s.check() == z3.sat

            m = s.model()
            for v in push_count:
                res += m[v].as_long()

    return res


class TestDay1(unittest.TestCase):
    # def test_part1(self):
    #     self.assertEqual(part1("../data/sample/day10.txt"), 7)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day10.txt"), 33)


if __name__ == "__main__":
    # print("part 1:", part1("../data/day10.txt"))
    print("part 2:", part2("../data/day10.txt"))

    _ = unittest.main()
