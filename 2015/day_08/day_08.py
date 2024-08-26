import json
import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/8
"""


def part_1() -> Union[int, str]:
    original_total = 0
    unescaped_total = 0

    for line in input_lines(INPUT_PATH):
        original_total += len(line)
        exec(f"un_escaped = {line}", globals())
        unescaped_total += len(un_escaped)

    return original_total - unescaped_total


def part_2() -> Union[int, str]:
    original_total = 0
    escaped_total = 0

    for line in input_lines(INPUT_PATH):
        original_total += len(line)
        escaped_total += len(json.dumps(line))

    return escaped_total - original_total


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
