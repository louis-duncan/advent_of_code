import math
import re
from math import inf
from pathlib import Path
from typing import Union, Iterator, Optional, Type, Any

"""
https://adventofcode.com/2023/day/6
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


def calc_distance(time_total: int, time_held: int) -> int:
    run_time = time_total - time_held
    return run_time * time_held


def part_1() -> Union[int, str]:
    lines = list(input_lines(Path("input.txt")))
    line_1_nums = [int(n) for n in re.findall(r"\b\d+\b", lines[0])]
    line_2_nums = [int(n) for n in re.findall(r"\b\d+\b", lines[1])]
    races = list(zip(line_1_nums, line_2_nums))

    num_options: list[int] = []
    for race in races:
        winning_times: list[int] = []
        for i in range(race[0]):
            distance = calc_distance(race[0], i)
            if distance > race[1]:
                winning_times.append(i)
            else:
                if len(winning_times):
                    break
        num_options.append(len(winning_times))

    return math.prod(num_options)


def part_2() -> Union[int, str]:
    lines = list(input_lines(Path("input.txt")))
    race_time = int("".join(re.findall(r"\b\d+\b", lines[0])))
    race_score = int("".join(re.findall(r"\b\d+\b", lines[1])))

    winning_times_start: int = 0
    winning_times_end: int = 0
    for i in range(race_time):
        distance = calc_distance(race_time, i)
        if distance > race_score:
            winning_times_start = i
            break

    for i in range(race_time, 0, -1):
        distance = calc_distance(race_time, i)
        if distance > race_score:
            winning_times_end = i
            break

    print(winning_times_start)
    print(winning_times_end)
    return winning_times_end - (winning_times_start - 1)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print()
    print("Part 2:", part_2())
