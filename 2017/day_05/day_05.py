import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2017/day/5
"""

_INPUT_PATH = INPUT_PATH  # TEST


def part_1() -> Union[int, str]:
    jumps: list[int] = list(input_lines(_INPUT_PATH, int))
    pos = 0
    count = 0
    while 0 <= pos < len(jumps):
        count += 1
        q = pos
        pos += jumps[pos]
        jumps[q] += 1
    return count


def part_2() -> Union[int, str]:
    jumps: list[int] = list(input_lines(_INPUT_PATH, int))
    pos = 0
    count = 0
    while 0 <= pos < len(jumps):
        count += 1
        q = pos
        pos += jumps[pos]
        if jumps[q] >= 3:
            jumps[q] -= 1
        else:
            jumps[q] += 1
    return count


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
