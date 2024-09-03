import time
from itertools import pairwise

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2017/day/1
"""


def part_1() -> Union[int, str]:
    input_text = raw_input("input.txt")
    digits = [int(v) for v in input_text]
    digits.append(digits[0])
    total = 0
    for a, b in pairwise(digits):
        if a == b:
            total += a
    return total


def part_2() -> Union[int, str]:
    input_text = raw_input("input.txt")
    digits = [int(v) for v in input_text]
    total = 0
    for a, b in zip(digits, digits[-len(digits) // 2:] + digits[:-len(digits) // 2]):
        if a == b:
            total += a
    return total


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
