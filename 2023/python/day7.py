import unittest
import math
from functools import cmp_to_key

all_cards_1 = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
all_cards_2 = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


def score_hand(cards):
    if all([True if card == cards[0] else False for card in cards]):
        return 1

    # check 4 of a kind
    if (
        sum([1 if card == cards[0] else 0 for card in cards]) == 4
        or sum([1 if card == cards[1] else 0 for card in cards]) == 4
    ):
        return 2

    counts = {}
    for card in cards:
        if card in counts:
            counts[card] += 1
        else:
            counts[card] = 1

    pairs = 0
    for card in counts:
        if counts[card] == 2:
            pairs += 1

    # full house
    if pairs == 1 and len(counts) == 2:
        return 3

    if (
        sum([1 if card == cards[0] else 0 for card in cards]) == 3
        or sum([1 if card == cards[1] else 0 for card in cards]) == 3
        or sum([1 if card == cards[2] else 0 for card in cards]) == 3
    ):
        return 4

    if pairs == 2:
        return 5

    if pairs == 1:
        return 6

    return 7


def compare_hands(hand1, hand2, part2=False):
    score1 = score_hand_2(hand1) if part2 else score_hand(hand1)
    score2 = score_hand_2(hand2) if part2 else score_hand(hand2)

    if score1 < score2:
        return 1
    elif score1 > score2:
        return -1
    else:
        return tiebreak(hand1, hand2, all_cards_2 if part2 else all_cards_1)


def tiebreak(hand1, hand2, card_value_list):
    for x, y in zip(hand1, hand2):
        if card_value_list.index(x) > card_value_list.index(y):
            return 1
        elif card_value_list.index(x) < card_value_list.index(y):
            return -1
    return 0


def part1(path):
    hands = []

    with open(path, "r") as file:
        for line in file.readlines():
            cards = list(line.split()[0])
            bid = line.split()[1]
            hands.append((cards, bid))

    sorted_hands = sorted(hands, key=cmp_to_key(lambda x, y: compare_hands(x[0], y[0])))

    score = 0
    for i, hand in enumerate(sorted_hands):
        score += (i + 1) * int(hand[1])
    return score


def possible_hands_wild(cards):
    if "J" not in cards:
        return [cards]

    for i, card in enumerate(cards):
        if card == "J":
            res = []
            for c in all_cards_2[1:]:
                new_cards = cards.copy()
                new_cards[i] = c
                res += possible_hands_wild(new_cards)
            return res


def score_hand_2(cards):
    min_score = 10  # not possible

    if "J" in cards:
        possible_hands = possible_hands_wild(cards)
        # print(len(possible_hands))
        for h in possible_hands:
            min_score = min(min_score, score_hand(h))

    return min(min_score, score_hand(cards))


def part2(path):
    hands = []

    with open(path, "r") as file:
        for line in file.readlines():
            cards = list(line.split()[0])
            bid = line.split()[1]
            hands.append((cards, bid))

    sorted_hands = sorted(
        hands, key=cmp_to_key(lambda x, y: compare_hands(x[0], y[0], True))
    )

    # for hand in sorted_hands:
    # print(hand, score_hand_2(hand[0]))

    score = 0
    for i, hand in enumerate(sorted_hands):
        score += (i + 1) * int(hand[1])
    return score


class TestDay(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1("../data/sample/day7.txt"), 6592)

    def test_part2(self):
        self.assertEqual(part2("../data/sample/day7.txt"), 6839)


if __name__ == "__main__":
    import time

    p1start = time.time()
    print("part 1:", part1("../data/day7.txt"))
    p1end = time.time()
    p2start = time.time()
    print("part 2:", part2("../data/day7.txt"))
    p2end = time.time()
    print("part 1 time:", p1end - p1start)
    print("part 2 time:", p2end - p2start)

    unittest.main()
