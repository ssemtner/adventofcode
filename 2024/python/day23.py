from collections import defaultdict
import time
import unittest
from itertools import combinations


def prepare(path):
    adj = defaultdict(set)
    with open(path) as file:
        for line in file.readlines():
            a, b = line.strip().split("-")
            adj[a].add(b)
            adj[b].add(a)
    return adj


def part1(path):
    res = 0
    adj = prepare(path)
    for a, b, c in combinations(adj.keys(), 3):
        if not (a[0] == "t" or b[0] == "t" or c[0] == "t"):
            continue
        if b in adj[a] and c in adj[b] and a in adj[c]:
            res += 1

    return res


# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
# given disjoint sets R, P, X, finds maximal cliques with all of R, some of P, none of X
def bron_kerbosch(adj: dict[str, set[str]], r: set[str], p: set[str], x: set[str]):
    if len(p) == 0 and len(x) == 0:
        return r

    (d, pivot) = max([(len(adj[v]), v) for v in p.union(x)])

    best = {}
    for v in p.difference(adj[pivot]):
        res = bron_kerbosch(
            adj, r.union({v}), p.intersection(adj[v]), x.intersection(adj[v])
        )
        if len(res) > len(best):
            best = res
        p.remove(v)
        p.add(v)

    return best


def part2(path):
    adj = prepare(path)
    clique = bron_kerbosch(adj, set(), set(adj.keys()), set())
    return ",".join(sorted(clique))


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day23.txt"), 7)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day23.txt"), "co,de,ka,ta")


if __name__ == "__main__":
    start = time.time()
    print(f"part 1: {part1('../data/day23.txt')} ({time.time() - start:.4f}s)")

    start = time.time()
    print(f"part 2: \"{part2('../data/day23.txt')}\" ({time.time() - start:.4f}s)")

    unittest.main()
