import json
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/12
"""

_INPUT_PATH = INPUT_PATH


def get_total(data, ignore=None) -> int:
    if isinstance(data, int):
        return data

    elif isinstance(data, list):
        total = 0

        for element in data:
            total += get_total(element, ignore)

        return total

    elif isinstance(data, dict):
        total = 0

        if ignore not in data.values():
            for element in data.values():
                total += get_total(element, ignore)

        return total

    else:
        return 0


def part_1() -> Union[int, str]:
    data = json.loads(raw_input(_INPUT_PATH))
    return get_total(data)


def part_2() -> Union[int, str]:
    data = json.loads(raw_input(_INPUT_PATH))
    return get_total(data, "red")


if __name__ == "__main__":
    p1_start = time.time()
    part_1_answer = part_1()
    p1_duration = time.time() - p1_start
    if part_1_answer is not None:
        print(f"Part 1 ({p1_duration * 1000:.2f}ms):", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    p2_start = time.time()
    part_2_answer = part_2()
    p2_duration = time.time() - p2_start
    if part_2_answer is not None:
        print(f"Part 2 ({p2_duration * 1000:.2f}ms):", part_2_answer)
        pyperclip.copy(part_2_answer)
