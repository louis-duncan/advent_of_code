import operator
import time

import pyperclip

from aoc_utils import *


OPERATORS: dict[str, Callable] = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
    "inc": operator.add,
    "dec": operator.sub,
}


"""
https://adventofcode.com/2017/day/8
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    registers: dict[str, int] = {}
    for line in input_lines(_INPUT_PATH):
        parts = line.strip().split(" ")
        reg, op, v_str, _, q, condition_str, p_str = parts
        v = int(v_str)
        p = int(p_str)
        condition = OPERATORS[condition_str]

        if condition(registers.get(q, 0), p):
            registers[reg] = OPERATORS[op](registers.get(reg, 0), v)

    return max(registers.values())


def part_2() -> Union[int, str]:
    registers: dict[str, int] = {}
    max_value = 0
    for line in input_lines(_INPUT_PATH):
        parts = line.strip().split(" ")
        reg, op, v_str, _, q, condition_str, p_str = parts
        v = int(v_str)
        p = int(p_str)
        condition = OPERATORS[condition_str]

        if condition(registers.get(q, 0), p):
            registers[reg] = OPERATORS[op](registers.get(reg, 0), v)
            if registers[reg] > max_value:
                max_value = registers[reg]

    return max_value


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
