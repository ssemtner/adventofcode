import time
import unittest
from dataclasses import dataclass
from itertools import pairwise, product
from functools import cache


@dataclass
class Pad:
    coords: dict[str, tuple[int, int]]
    gap: tuple[int, int]


def create_pad(rows):
    coords = {}
    gap = (-1, -1)
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            if c == " ":
                gap = (i, j)
            else:
                coords[c] = (i, j)
    return Pad(coords, gap)


NUM_PAD = create_pad(["789", "456", "123", " 0A"])
DIR_PAD = create_pad([" ^A", "<v>"])


def optimal(k1, k2, pad: Pad):
    i1, j1 = pad.coords[k1]
    i2, j2 = pad.coords[k2]

    di = "^" * (i1 - i2) if i1 > i2 else "v" * (i2 - i1)
    dj = "<" * (j1 - j2) if j1 > j2 else ">" * (j2 - j1)

    if j2 > j1 and (i2, j1) != pad.gap:
        return di + dj + "A"
    if (i1, j2) != pad.gap:
        return dj + di + "A"
    else:
        return di + dj + "A"


def sequences(seq, pad: Pad):
    for p, n in pairwise("A" + seq):
        yield optimal(p, n, pad)


def part1(path):
    with open(path) as file:
        res = 0
        for line in file.readlines():
            line = line.strip()
            dirs_1 = "".join(sequences(line, NUM_PAD))
            dirs_2 = "".join(sequences(dirs_1, DIR_PAD))
            dirs_3 = "".join(sequences(dirs_2, DIR_PAD))
            res += len(dirs_3) * int(line[:-1])

    return res


def part2(path):
    @cache
    def get_counts(seq):
        counts: dict[str, int] = {}
        for i in sequences(seq, DIR_PAD):
            counts[i] = counts.get(i, 0) + 1
        return counts

    with open(path) as file:
        res = 0
        for line in file.readlines():
            line = line.strip()

            counts = {"".join(sequences(line, NUM_PAD)): 1}

            for _ in range(25):
                new_counts = {}
                for k, v in counts.items():
                    for s, c in get_counts(k).items():
                        new_counts[s] = new_counts.get(s, 0) + v * c
                counts = new_counts

            res += int(line[:-1]) * sum(len(k) * v for k, v in counts.items())
        return res


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day21.txt"), 126384)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day21.txt"), 154115708116294)


if __name__ == "__main__":
    start = time.time()
    print(f"part 1: {part1('../data/day21.txt')} ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: {part2('../data/day21.txt')} ({time.time() - start:.4f}s)")

    unittest.main()
