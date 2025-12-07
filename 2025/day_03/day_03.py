import itertools
import time
from typing import Union

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/3
"""

_INPUT_PATH = au.INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    lines = au.input_lines(_INPUT_PATH)

    jolts_sum = 0

    for bank in lines:
        biggest = 0
        for comb in itertools.combinations(bank, 2):
            v = int("".join(comb))
            if v > biggest:
                biggest = v
            if biggest == 99:
                break

        jolts_sum += biggest

    return jolts_sum


def part_2() -> Union[int, str]:
    lines = au.input_lines(_INPUT_PATH)

    jolts_sum = 0

    for i, bank in enumerate(lines):
        print(i)
        biggest_int = 0
        biggest_str = "0"
        for comb in itertools.combinations(bank, 12):
            if comb[0] < biggest_str[0]:
                continue
            v = int("".join(comb))
            if v > biggest_int:
                biggest_int = v
                biggest_str = str(v)
            if biggest_int == 999999999999:
                break

        jolts_sum += biggest_int

    return jolts_sum


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
