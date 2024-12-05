import time
from itertools import pairwise

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/2
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def same_sign(a, b):
    return a * b > 0


def is_safe(nums) -> tuple[bool, int]:
    test_diff = nums[0] - nums[1]
    for i, (a, b) in enumerate(pairwise(nums)):
        diff = a - b
        if not same_sign(diff, test_diff):
            return False, i
        if not (1 <= abs(diff) <= 3):
            return False, i
    return True, 0


def part_1() -> Union[int, str]:
    safe_count = 0

    for line in input_lines(_INPUT_PATH):
        nums = [int(n) for n in line.strip().split(" ")]
        safe, _ = is_safe(nums)
        safe_count += int(safe)

    return safe_count


def part_2() -> Union[int, str]:
    safe_count = 0

    for line in input_lines(_INPUT_PATH):
        nums = [int(n) for n in line.strip().split(" ")]
        safe, i = is_safe(nums)
        if not safe:
            try:
                safe, _ = is_safe(nums[:i] + nums[i+1:])
            except IndexError:
                pass
            if not safe:
                try:
                    safe, _= is_safe(nums[:i+1] + nums[i+2:])
                except IndexError:
                    pass
                if not safe:
                    safe, _ = is_safe(nums[1:])
        safe_count += int(safe)

    return safe_count


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
