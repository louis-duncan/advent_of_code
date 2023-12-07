from pathlib import Path
from typing import Union, Iterator, Optional, Type, Any
from enum import Enum

"""
https://adventofcode.com/2023/day/7
"""


class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __lt__(self, other):
        return self.value < other.value


class Hand:
    def __init__(self, line: str, enable_joker=False):
        _cards, _bid = line.strip().split(" ")
        self.cards = str(_cards)
        self.bid = int(_bid)

        self._enable_joker = enable_joker
        self.non_int_cards = {
            "T": 10,
            "J": 11 if not enable_joker else 1,
            "Q": 12,
            "K": 13,
            "A": 14
        }

        self.type = self._type()

    def _split_cards(self) -> dict[str, int]:
        parts = {}
        for c in self.cards:
            parts[c] = self.cards.count(c)
        return parts

    def _type(self) -> HandType:
        parts = self._split_cards()

        if 5 in parts.values():
            return HandType.FIVE_OF_A_KIND  # All cards the same, 5 of a kind even if J
        elif 4 in parts.values():
            current = HandType.FOUR_OF_A_KIND
        elif 3 in parts.values() and 2 in parts.values():
            current = HandType.FULL_HOUSE
        elif 3 in parts.values():
            current = HandType.THREE_OF_A_KIND
        elif list(parts.values()).count(2) == 2:
            current = HandType.TWO_PAIR
        elif 2 in parts.values():
            current = HandType.ONE_PAIR
        else:
            current = HandType.HIGH_CARD

        if (not self._enable_joker) or ('J' not in parts):
            return current

        num_jokers = parts['J']
        parts.pop('J')
        highest_count = max(parts.values())
        for k in parts:
            if parts[k] == highest_count:
                parts[k] += num_jokers
                break

        if 5 in parts.values():
            possible = HandType.FIVE_OF_A_KIND
        elif 4 in parts.values():
            possible = HandType.FOUR_OF_A_KIND
        elif 3 in parts.values() and 2 in parts.values():
            possible = HandType.FULL_HOUSE
        elif 3 in parts.values():
            possible = HandType.THREE_OF_A_KIND
        elif list(parts.values()).count(2) == 2:
            possible = HandType.TWO_PAIR
        elif 2 in parts.values():
            possible = HandType.ONE_PAIR
        else:
            possible = HandType.HIGH_CARD

        if possible.value > current.value:
            return possible
        else:
            return current

    def _card_value(self, card: str):
        try:
            return int(card)
        except ValueError:
            pass
        try:
            return self.non_int_cards[card]
        except KeyError:
            raise ValueError(f"'{card}' is not a valid card")

    @property
    def values(self) -> tuple[int, ...]:
        values: tuple[int, ...] = tuple([self._card_value(c) for c in self.cards])
        assert len(values) == 5
        return values

    def __gt__(self, other):
        assert isinstance(other, Hand)
        if self.type == other.type:
            return self.values > other.values
        else:
            return self.type > other.type

    def __lt__(self, other):
        assert isinstance(other, Hand)
        if self.type == other.type:
            return self.values < other.values
        else:
            return self.type < other.type

    def __eq__(self, other):
        assert isinstance(other, Hand)
        if self.type == other.type:
            return self.cards == other.cards
        else:
            return False

    def __repr__(self):
        return f"Hand(cards={repr(self.cards)}, bid={repr(self.bid)}, type={repr(self.type)})"


def raw_input(input_path: Path = Path("input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read()
    return data


def input_lines(input_path: Path = Path("input.txt"), convert_type: Optional[Type] = None) -> Iterator[Any]:
    for line in raw_input(input_path).strip().split("\n"):
        if convert_type is None:
            yield line.strip()
        else:
            yield convert_type(line.strip())


def part_1() -> Union[int, str]:
    hands = [Hand(line) for line in input_lines(Path("input.txt"))]
    scores = []
    for i, h in enumerate(sorted(hands)):
        scores.append((i + 1) * h.bid)
    return sum(scores)


def part_2() -> Union[int, str]:
    hands = [Hand(line, enable_joker=True) for line in input_lines(Path("input.txt"))]

    scores = []
    for i, h in enumerate(sorted(hands)):
        scores.append((i + 1) * h.bid)
    return sum(scores)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print()
    print("Part 2:", part_2())
