import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/1
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    list_1 = []
    list_2 = []
    for line in input_lines(_INPUT_PATH):
        p1, p2 = line.strip().split("   ")
        list_1.append(int(p1))
        list_2.append(int(p2))
    return sum((abs(a-b) for a, b in zip(sorted(list_1), sorted(list_2))))


def part_2() -> Union[int, str]:
    list_1 = []
    list_2 = []
    for line in input_lines(_INPUT_PATH):
        p1, p2 = line.strip().split("   ")
        list_1.append(int(p1))
        list_2.append(int(p2))
    return sum((list_2.count(a) * a for a in list_1))


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
