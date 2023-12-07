from enum import Enum
from functools import cached_property
from math import floor
import re
import sys
from typing import Optional

CARD_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    def __int__(self):
        return self.value


class Hand:
    def __init__(self, cards: str, bid: int) -> None:
        assert len(cards) == 5
        assert bid > 0

        self._cards = cards
        self._bid = bid

    def bid(self) -> int:
        return self._bid

    @cached_property
    def card_values(self) -> list[int]:
        return [CARD_VALUES[card] for card in self._cards]

    @cached_property
    def hand_type(self) -> HandType:
        index = {}
        for c in self._cards:
            if not c in index:
                index[c] = 0
            index[c] += 1

        by_count: map[int, list[str]] = {}
        for i in range(0, len(self._cards) + 1):
            by_count[i] = []

        for card in index:
            by_count[index[card]].append(card)

        if len(by_count[5]) == 1:
            return HandType.FIVE_OF_A_KIND
        elif len(by_count[4]) == 1:
            return HandType.FOUR_OF_A_KIND
        elif len(by_count[3]) == 1 and len(by_count[2]) == 1:
            return HandType.FULL_HOUSE
        elif len(by_count[3]) == 1:
            return HandType.THREE_OF_A_KIND
        elif len(by_count[2]) == 2:
            return HandType.TWO_PAIR
        elif len(by_count[2]) == 1:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    @staticmethod
    def key(x: "Hand") -> list[int]:
        return [int(x.hand_type), *x.card_values]


def parse_input(lines) -> list[Hand]:
    result = []
    for line in lines:
        cards, bid = line.split(" ")
        result.append(Hand(cards, int(bid)))
    return result


def part1(lines):
    hands = parse_input(lines)
    result = 0
    for rank, hand in enumerate(sorted(hands, key=Hand.key)):
        result += hand.bid() * (rank + 1)

    return result


def part2(lines):
    pass


if __name__ == "__main__":
    lines = (line.strip() for line in sys.stdin)
    lines = [line for line in lines if line != ""]
    print(part1(lines))
    print(part2(lines))
