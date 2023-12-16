from enum import Enum
from collections import Counter, namedtuple
from typing import List

HandToBid = namedtuple("HandToBid", ("hand", "bid"))


class Rank(Enum):
    HIGH = 1
    ONE = 2
    TWO = 3
    THREE = 4
    FULL = 5
    FOUR = 6
    FIVE = 7


SORTED_CARD_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']


GROUPED_CARD_COUNTS_TO_RANKS = {
            (5,): Rank.FIVE,
            (1, 4): Rank.FOUR,
            (2, 3): Rank.FULL,
            (1, 1, 3): Rank.THREE,
            (1, 2, 2): Rank.TWO,
            (1, 1, 1, 2): Rank.ONE,
            (1, 1, 1, 1, 1): Rank.HIGH
}


class Hand:
    def __init__(self, rank, numerical_weight, cards):
        self.rank = rank
        self.numerical_weight = numerical_weight
        self.cards = cards

    @classmethod
    def create_from_cards(cls, cards: str):
        rank = cls.determine_rank(cards)
        numerical_weight = cls.get_numerical_weight(rank, cards)
        return Hand(rank, numerical_weight, cards)

    @classmethod
    def determine_rank(cls, cards):
        counted_cards = Counter(cards)
        sorted_counts = tuple(sorted(counted_cards.values()))
        return GROUPED_CARD_COUNTS_TO_RANKS[sorted_counts]

    @classmethod
    def get_numerical_weight(cls, rank, cards):
        card_weights = [SORTED_CARD_VALUES.index(card) for card in cards]
        str_weight = f"{rank.value}."
        for card_weight in card_weights:
            str_weight += f"{card_weight:02d}"
        return float(str_weight)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Rank(cards={self.cards}, rank={self.rank}, weight={self.numerical_weight})"


def part_1(lines: List[str]) -> int:
    hand_to_bid_list = []
    for line in lines:
        hand_str, bid_str = line.split(" ")
        hand_to_bid_list.append(
            HandToBid(
                Hand.create_from_cards(hand_str),
                int(bid_str)
            )
        )
    hand_to_bid_list.sort(key=lambda hand_to_bid: hand_to_bid.hand.numerical_weight)
    final_score = sum([hand_to_bid.bid * (index + 1) for index, hand_to_bid in enumerate(hand_to_bid_list)])
    return final_score
