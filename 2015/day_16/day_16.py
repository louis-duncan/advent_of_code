import itertools
import time
from itertools import pairwise

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/16
"""

_INPUT_PATH = INPUT_PATH


def part_1() -> Union[int, str]:
    present_known = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }

    for i, line in enumerate(input_lines(_INPUT_PATH)):
        if i == 80:
            pass
        _, info = line.split(":", 1)
        parts = [p.strip(": ,") for p in info.strip().split(" ")]
        is_aunt = True
        for fact_name, value in itertools.batched(parts, 2):
            try:
                if present_known[fact_name] != int(value):
                    is_aunt = False
                    break
            except KeyError:
                pass
        if is_aunt:
            return i + 1


def part_2() -> Union[int, str]:
    present_known = {
        'children': lambda x: x == 3,
        'cats': lambda x: x > 7,
        'samoyeds': lambda x: x == 2,
        'pomeranians': lambda x: x < 3,
        'akitas': lambda x: x == 0,
        'vizslas': lambda x: x == 0,
        'goldfish': lambda x: x < 5,
        'trees': lambda x: x > 3,
        'cars': lambda x: x == 2,
        'perfumes': lambda x: x == 1
    }

    for i, line in enumerate(input_lines(_INPUT_PATH)):
        if i == 80:
            pass
        _, info = line.split(":", 1)
        parts = [p.strip(": ,") for p in info.strip().split(" ")]
        is_aunt = True
        for fact_name, value in itertools.batched(parts, 2):
            try:
                if not present_known[fact_name](int(value)):
                    is_aunt = False
                    break
            except KeyError:
                pass
        if is_aunt:
            return i + 1


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
