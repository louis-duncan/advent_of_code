import itertools
import operator
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/7
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def resolve(values: list[int], operators: Union[list[Callable], tuple[Callable, ...]]) -> int:
    result = values[0]
    assert len(values) == len(operators) + 1
    for op, v in zip(operators, values[1:]):
        result = op(result, v)
    return result


def part_1() -> Union[int, str]:
    operators = [operator.add, operator.mul]
    result = 0
    for line in input_lines(_INPUT_PATH):
        parts = line.split(" ")
        target = int(parts[0].strip(":"))
        values = [int(v) for v in parts[1:]]
        for ops in list(itertools.product(operators, repeat=len(values) - 1)):
            if resolve(values, ops) == target:
                result += target
                break
    return result


def part_2() -> Union[int, str]:
    def concat(v1, v2):
        return int(str(v1) + str(v2))

    operators = [operator.add, operator.mul, concat]
    result = 0
    for line in input_lines(_INPUT_PATH):
        parts = line.split(" ")
        target = int(parts[0].strip(":"))
        values = [int(v) for v in parts[1:]]
        for ops in list(itertools.product(operators, repeat=len(values) - 1)):
            if resolve(values, ops) == target:
                result += target
                break
    return result


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
