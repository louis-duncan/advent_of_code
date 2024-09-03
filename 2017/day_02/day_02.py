import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2017/day/2
"""


def part_1() -> Union[int, str]:
    total = 0
    for line in input_lines("input.txt"):
        numbers = [int(v) for v in line.split("\t")]
        total += max(numbers) - min(numbers)
    return total

def part_2() -> Union[int, str]:
    def find_value(_numbers: list[int]) -> int:
        for i in range(len(_numbers) - 1):
            for j in range(i + 1, len(_numbers)):
                if _numbers[i] % _numbers[j] == 0:
                    return _numbers[i] // _numbers[j]
        raise ValueError(f"Found no answer for numbers: {_numbers}")

    total = 0
    for line in input_lines("input.txt"):
        numbers = sorted([int(v) for v in line.split("\t")], reverse=True)
        total += find_value(numbers)

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
