from functools import reduce
import time

import pyperclip

from aoc_utils import *



"""
https://adventofcode.com/2015/day/20
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def factors(n):
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def part_1() -> Union[int, str]:
    target = int(int(raw_input(_INPUT_PATH).strip()) / 10)

    t = 0
    n = 0
    step = 12
    while t < target:
        n += step
        t = sum(factors(n))

    return n


def part_2() -> Union[int, str]:
    target = int(int(raw_input(_INPUT_PATH).strip()) / 11)

    t = 0
    n = 0
    step = 12
    house_limit = 50
    while t < target:
        n += step
        t = sum([f for f in factors(n) if n <= house_limit * f])

    return n


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
