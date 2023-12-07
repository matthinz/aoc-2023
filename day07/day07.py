from enum import Enum
from functools import cached_property
from math import floor
import re
import sys
from typing import Generator, Optional

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
    def __init__(self, cards: str, bid: int, jokers_wild) -> None:
        assert len(cards) == 5
        assert bid > 0

        self._cards = cards
        self._bid = bid
        self._jokers_wild = jokers_wild

    def bid(self) -> int:
        return self._bid

    @cached_property
    def card_values(self) -> Generator[int, None, None]:
        for card in self._cards:
            if self._jokers_wild and card == "J":
                yield 0
            else:
                yield CARD_VALUES[card]

    @cached_property
    def hand_type(self) -> HandType:
        cards = self._cards
        jokers = 0

        if self._jokers_wild:
            jokers = self._cards.count("J")
            cards = self._cards.replace("J", "")

        counts = {}
        for i in range(0, len(self._cards) + 1):
            counts[i] = []

        for card in set(cards):
            count = cards.count(card)
            counts[count].append(card)

        if len(counts[5]) == 1:
            return HandType.FIVE_OF_A_KIND

        if len(counts[4]) == 1:
            if jokers == 1:
                return HandType.FIVE_OF_A_KIND
            else:
                return HandType.FOUR_OF_A_KIND

        if len(counts[3]) == 1:
            if jokers == 2:
                return HandType.FIVE_OF_A_KIND
            elif jokers == 1:
                return HandType.FOUR_OF_A_KIND
            elif len(counts[2]) == 1:
                return HandType.FULL_HOUSE
            else:
                return HandType.THREE_OF_A_KIND

        if len(counts[2]) == 2:
            if jokers == 1:
                return HandType.FULL_HOUSE
            else:
                return HandType.TWO_PAIR

        if len(counts[2]) == 1:
            if jokers == 3:
                return HandType.FIVE_OF_A_KIND
            elif jokers == 2:
                return HandType.FOUR_OF_A_KIND
            elif jokers == 1:
                return HandType.THREE_OF_A_KIND
            else:
                return HandType.ONE_PAIR

        # We have no pairs
        match jokers:
            case 5:
                return HandType.FIVE_OF_A_KIND
            case 4:
                return HandType.FIVE_OF_A_KIND
            case 3:
                return HandType.FOUR_OF_A_KIND
            case 2:
                return HandType.THREE_OF_A_KIND
            case 1:
                return HandType.ONE_PAIR

        return HandType.HIGH_CARD

    @staticmethod
    def key(x: "Hand") -> list[int]:
        return [int(x.hand_type), *x.card_values]


def parse_input(lines, jokers_wild) -> list[Hand]:
    result = []
    for line in lines:
        cards, bid = line.split(" ")
        result.append(Hand(cards, int(bid), jokers_wild=jokers_wild))
    return result


def part1(lines):
    hands = parse_input(lines, jokers_wild=False)
    result = 0
    for rank, hand in enumerate(sorted(hands, key=Hand.key)):
        result += hand.bid() * (rank + 1)

    return result


def part2(lines):
    hands = parse_input(lines, jokers_wild=True)
    result = 0
    for rank, hand in enumerate(sorted(hands, key=Hand.key)):
        result += hand.bid() * (rank + 1)

    return result


if __name__ == "__main__":
    lines = (line.strip() for line in sys.stdin)
    lines = [line for line in lines if line != ""]
    print(part1(lines))
    print(part2(lines))
