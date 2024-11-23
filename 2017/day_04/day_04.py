import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2017/day/4
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    pass_phrases = input_lines(_INPUT_PATH)
    valid_count = 0
    for phrase in pass_phrases:
        parts = phrase.strip().split(" ")
        if len(set(parts)) == len(parts):
            valid_count += 1
    return valid_count


def part_2() -> Union[int, str]:
    pass_phrases = input_lines(_INPUT_PATH)
    valid_count = 0
    for phrase in pass_phrases:
        parts = ["".join(sorted(list(p))) for p in phrase.strip().split(" ")]
        if len(set(parts)) == len(parts):
            valid_count += 1
    return valid_count


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
