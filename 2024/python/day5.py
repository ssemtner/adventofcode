import unittest
from collections import defaultdict


def issue(rules, update):
    s = set(update)
    seen = set()
    for x in update:
        if x in s:  # only care about rule if both are present
            for y in rules[x]:
                if y in s and y not in seen:
                    return (x, y)
        seen.add(x)
    return None


def parse(path):
    with open(path) as file:
        text = file.read().strip()
    rules, updates = text.split("\n\n")
    rules_l = [[int(x) for x in rule.split("|")] for rule in rules.split("\n")]
    # all in list of rules[x] need to go before x
    rules = defaultdict(list)
    for rule in rules_l:
        rules[rule[1]].append(rule[0])
    updates = [[int(x) for x in update.split(",")] for update in updates.split("\n")]

    return rules, updates


def part1(path):
    rules, updates = parse(path)

    res = 0
    for update in updates:
        if issue(rules, update) is None:
            res += update[len(update) // 2]
    return res


def part2(path):
    rules, updates = parse(path)

    res = 0
    for update in updates:
        if issue(rules, update) is not None:
            # just swap problems until it's good
            while issue(rules, update) is not None:
                x, y = issue(rules, update)
                x_i = update.index(x)
                y_i = update.index(y)
                update[x_i], update[y_i] = update[y_i], update[x_i]
            res += update[len(update) // 2]

    return res


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day5.txt"), 143)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day5.txt"), 123)


if __name__ == "__main__":
    print("part 1:", part1("../data/day5.txt"))
    print("part 2:", part2("../data/day5.txt"))

    unittest.main()
