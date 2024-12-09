import unittest


def prep(path):
    with open(path) as file:
        lines = file.readlines()
        t = lines[0].strip()
        data = []
        for i in range(len(t)):
            if i % 2 == 0:
                data.append([i // 2, int(t[i])])
            else:
                data.append([None, int(t[i])])
    return data


def checksum(data):
    real = []
    for entry in data:
        real.extend([entry[0] for _ in range(entry[1])])
    res = 0
    for i in range(len(real)):
        if real[i] is not None:
            res += real[i] * i
    return res


def part1(path):
    data = prep(path)

    di = len(data) - 1
    a = 0
    # go through backwards
    while di >= a:
        while data[a][0] is not None:
            a += 1
        while data[di][0] is None:
            di -= 1

        need = data[di][1]
        have = data[a][1]
        using = min(need, have)
        data[di][1] -= using
        data[a] = (data[di][0], using)
        if using < have:
            data.insert(a + 1, (None, have - using))
            di += 1
            a += 1
        if data[di][1] == 0:
            di -= 1

    return checksum(data)


def part2(path):
    data = prep(path)

    di = len(data) - 1
    while di >= 0:
        while data[di][0] is None:
            di -= 1
        need = data[di][1]

        a = 0
        broke = False
        # really show search this is where the entire 2s runtime comes from
        while data[a][0] is not None or data[a][1] < need:
            a += 1
            if a >= di:
                broke = True
                break
        if broke:
            di -= 1
            continue
        have = data[a][1]
        data[a][0] = data[di][0]
        data[a][1] = data[di][1]
        data[di][0] = None

        if have > need:
            data.insert(a + 1, [None, have - need])
        else:
            di -= 1

    return checksum(data)


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day9.txt"), 1928)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day9.txt"), 2858)


if __name__ == "__main__":
    import time

    start = time.time()
    print(f"part 1: {part1('../data/day9.txt')} ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: {part2('../data/day9.txt')} ({time.time() - start:.4f}s)")

    unittest.main()
