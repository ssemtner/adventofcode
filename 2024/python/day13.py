import unittest
import re
import sympy
import time


def solve(path, p2):
    with open(path) as file:
        pattern = re.compile(r".*X.(\d+), Y.(\d+).*")
        sections = [
            [
                [int(x) for x in pattern.match(line).groups()]
                for line in text.split("\n")
            ]
            for text in file.read().strip().split("\n\n")
        ]

    res = 0
    for section in sections:
        ax, ay = section[0]
        bx, by = section[1]
        tx, ty = section[2]

        if p2:
            tx += 10**13
            ty += 10**13

        a, b = sympy.symbols("a b", integer=True)
        x_eq = sympy.Eq(ax * a + bx * b, tx)
        y_eq = sympy.Eq(ay * a + by * b, ty)
        sol = sympy.solve([x_eq, y_eq], (a, b))

        try:
            res += sol[a] * 3 + sol[b]
        except:
            pass

    return res


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(solve("../data/sample/day13.txt", False), 480)


if __name__ == "__main__":
    start = time.time()
    print(f"part 1: {solve('../data/day13.txt', False)} ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: {solve('../data/day13.txt', True)} ({time.time() - start:.4f}s)")

    unittest.main()
