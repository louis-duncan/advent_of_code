import itertools
import time
from typing import Union

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/9
"""

_INPUT_PATH = au.INPUT_PATH_TEST


def part_1() -> Union[int, str]:
    location_points: list[au.Point] = []
    for line in au.input_lines(test=False):
        parts = line.strip().split(",")
        location_points.append(au.Point("#", int(parts[0]), int(parts[1])))

    max_area = 0
    for a, b in itertools.combinations(location_points, 2):
        v = a - b
        a = (abs(v.dx) + 1) * (abs(v.dy) + 1)
        if a > max_area:
            max_area = a

    return max_area


def part_2() -> Union[int, str]:
    ...


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
