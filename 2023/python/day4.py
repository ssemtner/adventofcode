import unittest


def part1(path):
    with open(path, "r") as file:
        sum = 0

        for line in file.readlines():
            sides = line.split(":")[1].split("|")
            winners = [x for x in sides[0].strip().split(" ") if x != ""]
            have = [x for x in sides[1].strip().split(" ") if x != ""]

            quantity = len([x for x in winners if x in have])

            if quantity > 0:
                sum += 2 ** (quantity - 1)

        return sum


def score_card(cards, n, d=0):
    # print("score_card", n, cards[n], d)
    if n >= len(cards) - 1:
        # print("return 1")
        return 1
    
    score = cards[n]

    return 1 + sum([score_card(cards, i, d+1) for i in range(n + 1, n + 1 + score)])



def part2(path):
    with open(path, "r") as file:
        cards = []

        for line in file.readlines():
            sides = line.split(":")[1].split("|")
            winners = [x for x in sides[0].strip().split(" ") if x != ""]
            have = [x for x in sides[1].strip().split(" ") if x != ""]

            score = len([x for x in winners if x in have])
            cards.append(score)

        return sum([score_card(cards, n) for n in range(len(cards))])


class TestDay1(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day4.txt"), 13)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day4.txt"), 30)


if __name__ == "__main__":
    print("part 1:", part1("../data/day4.txt"))
    print("part 2:", part2("../data/day4.txt"))

    unittest.main()
