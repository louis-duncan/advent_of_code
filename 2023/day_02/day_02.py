import re
from pathlib import Path
from typing import Union, Iterator, Optional, Type, Any

"""
https://adventofcode.com/2023/day/2
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
    impossible_games = set()
    all_games = set()
    limits = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    for line in input_lines(Path("input.txt")):
        game_number = int(re.search(r"\d+(?=:)", line).group())
        all_games.add(game_number)
        groups = re.findall(r"\d+ .*?(?=;|$)", line)
        done = False
        for group in groups:
            pulls = group.split(", ")
            for pull in pulls:
                n, col = pull.split(" ")
                n = int(n)
                if n > limits[col]:
                    impossible_games.add(game_number)
                    done = True
                    break
            if done:
                break

    return sum(all_games.difference(impossible_games))


def mul(*args) -> int:
    args = list(args)
    if len(args) == 0:
        return 0

    total = args.pop()
    while len(args):
        total *= args.pop()

    return total


def part_2() -> Union[int, str]:
    game_powers = []
    for line in input_lines(Path("input.txt")):
        maxes = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        game_number = int(re.search(r"\d+(?=:)", line).group())
        groups = re.findall(r"\d+ .*?(?=;|$)", line)
        for group in groups:
            pulls = group.split(", ")
            for pull in pulls:
                n, col = pull.split(" ")
                n = int(n)
                if n > maxes[col]:
                    maxes[col] = n
        game_powers.append(mul(*maxes.values()))

    return sum(game_powers)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print()
    print("Part 2:", part_2())
