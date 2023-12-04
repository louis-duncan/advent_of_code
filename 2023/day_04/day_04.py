import re
from pathlib import Path
from typing import Union, Iterator, Optional, Type, Any

"""
https://adventofcode.com/2023/day/4
"""


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
    total = 0
    for card_line in input_lines(Path("input.txt")):
        winning_numbers_part = re.search(r"(\d+ *?)*(?= \|)", card_line).group()
        winning_numbers = [int(n) for n in re.findall(r"\d+", winning_numbers_part)]
        check_numbers_part = re.search(r"(\d+ *?)*(?=$)", card_line).group()
        check_numbers = [int(n) for n in (re.findall(r"\d+", check_numbers_part))]

        count = 0
        for cn in check_numbers:
            if cn in winning_numbers:
                count += 1
        if count:
            score = 2 ** (count - 1)
            total += score
        else:
            score = 0

    return total


def part_2() -> Union[int, str]:
    card_counts = {}
    for card_line in input_lines(Path("input.txt")):
        try:
            card_number = int(re.search(r"(?<= )\d+(?=:)", card_line).group())
            winning_numbers_part = re.search(r"(\d+ *?)*(?= \|)", card_line).group()
            winning_numbers = [int(n) for n in re.findall(r"\d+", winning_numbers_part)]
            check_numbers_part = re.search(r"(\d+ *?)*(?=$)", card_line).group()
            check_numbers = [int(n) for n in (re.findall(r"\d+", check_numbers_part))]
        except Exception as e:
            print(f"Error line: {card_line}")
            raise e

        count = 0
        for cn in check_numbers:
            if cn in winning_numbers:
                count += 1

        card_counts[card_number] = {
            'score': count,
            'qty': 1
        }

    num_cards = 0
    for card_number in card_counts:
        num_cards += card_counts[card_number]['qty']
        if card_counts[card_number]['score']:
            for i in range(card_number + 1, card_number + 1 + card_counts[card_number]['score']):
                card_counts[i]['qty'] += card_counts[card_number]['qty']

    return num_cards


if __name__ == "__main__":
    print("Part 1:", part_1())
    print()
    print("Part 2:", part_2())
