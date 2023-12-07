import unittest
import math
from functools import cmp_to_key

all_cards_1 = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
all_cards_2 = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


def score_hand(cards):
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

    if len(counts) == 1:
        return 1  # 5 of a kind

    # check 4 of a kind
    if len(counts) == 2:
        if pairs == 1:
            return 3  # full house
        else:
            return 2  # four of a kind

    if max(counts.values()) == 3:
        return 4  # 3 of a kind

    if pairs == 2:
        return 5  # 2 pairs

    if pairs == 1:
        return 6  # 1 pair

    return 7  # high card


def compare_hands(hand1, hand2, part2=False):
    score1 = score_hand_wilds(hand1) if part2 else score_hand(hand1)
    score2 = score_hand_wilds(hand2) if part2 else score_hand(hand2)

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


def score_hand_wilds(cards):
    counts = {}
    for card in cards:
        if card in counts:
            counts[card] += 1
        else:
            counts[card] = 1

    counts.pop("J", None)
    if len(counts) == 0:
        return score_hand(cards)
    most_common = max(counts.items(), key=lambda x: x[1])[0]
    return score_hand([most_common if c == "J" else c for c in cards])


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
