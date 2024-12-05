import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/3
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    total = 0
    for line in input_lines(_INPUT_PATH):
        for mul in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line):
            a, b = int(mul[0]), int(mul[1])
            total += a * b
    return total


def part_2() -> Union[int, str]:
    total = 0
    enabled = True
    for line in input_lines(_INPUT_PATH):
        for inst in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do(?:n't)?)", line):
            if inst[2] == "do":
                enabled = True
            elif inst[2] == "don't":
                enabled = False
            elif enabled:
                total += int(inst[0]) * int(inst[1])
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
