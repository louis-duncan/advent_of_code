import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/2
"""


def part_1() -> Union[int, str]:
    total = 0
    for line in input_lines(INPUT_PATH):
        a, b, c = sorted([int(n) for n in line.split("x")])
        total += 3 * a * b + 2 * b * c + 2 * a * c
    return total


def part_2() -> Union[int, str]:
    total = 0
    for line in input_lines(INPUT_PATH):
        a, b, c = sorted([int(n) for n in line.split("x")])
        vol = a * b * c
        total += 2 * a + 2 * b + vol
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
