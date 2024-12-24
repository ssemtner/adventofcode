import time
import unittest


def execute(program, initial_a):
    a, b, c = initial_a, 0, 0

    def combo(n: int) -> int:
        if n == 4:
            return a
        elif n == 5:
            return b
        elif n == 6:
            return c
        else:
            assert 0 <= n <= 3
            return n

    output = []

    i = 0
    while i < len(program):
        op = program[i]
        val = program[i + 1]
        match op:
            case 0:
                a = a // (2 ** combo(val))
            case 1:
                b = b ^ val
            case 2:
                b = combo(val) & 0b111
            case 3:
                if a != 0:
                    i = val
                    continue
            case 4:
                b = b ^ c
            case 5:
                output.append(combo(val) & 0b111)
            case 6:
                b = a // (2 ** combo(val))
            case 7:
                c = a // (2 ** combo(val))

        i += 2

    return output


def part1(path):
    with open(path) as file:
        lines = file.readlines()
    a, _, _ = [int(line.split()[-1]) for line in lines[:3]]
    program = [int(x) for x in lines[-1].split()[-1].split(",")]

    return ",".join(map(str, execute(program, a)))


def part2(path):
    with open(path) as file:
        lines = file.readlines()
    program = [int(x) for x in lines[-1].split()[-1].split(",")]
    target = program[::-1]

    def solve(a=0, depth=0):
        if depth == len(target):
            return a
        for i in range(8):
            output = execute(program, a * 8 + i)
            if output and output[0] == target[depth]:
                if result := solve((a * 8 + i), depth + 1):
                    return result
        return 0

    a = solve()
    output = execute(program, a)
    assert output == program

    return a


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day17part1.txt"), "4,6,3,5,6,3,5,2,1,0")

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day17part2.txt"), 117440)


if __name__ == "__main__":
    start = time.time()
    print(f"part 1: \"{part1('../data/day17.txt')}\" ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: {part2('../data/day17.txt')} ({time.time() - start:.4f}s)")

    unittest.main()
