import re
import time
from functools import cache

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/7
"""


def part_1() -> Union[int, str]:
    operations = {
        "AND": lambda a, b: a & b,
        "OR": lambda a, b: a | b,
        "LSHIFT": lambda a, b: a << b,
        "RSHIFT": lambda a, b : a >> b,
        "NOT": lambda a: 65535 - a,
        "=": lambda a: a
    }
    connections = {}

    for line in input_lines(INPUT_PATH):
        if m := re.match(r"(\w+) -> (\w+)", line):
            in_1, out = m.groups()
            connections[out] = ("=", in_1)
        elif m := re.match(r"([\w]+) ([A-Z]+) (\w+) -> (\w+)", line):
            in_1, op, in_2, out = m.groups()
            connections[out] = (op, in_1, in_2)
        elif m := re.match(r"NOT (\w+) -> (\w+)", line):
            in_1, out = m.groups()
            connections[out] = ("NOT", in_1)
        else:
            raise ValueError(f"Unknown operation: {line}")

    @cache
    def get_result(target: str) -> int:
        if target.isdecimal():
            return int(target)

        operation, *values = connections[target]
        resolved_values = [get_result(v) for v in values]
        return operations[operation](*resolved_values)

    return get_result("a")


def part_2() -> Union[int, str]:
    operations = {
        "AND": lambda a, b: a & b,
        "OR": lambda a, b: a | b,
        "LSHIFT": lambda a, b: a << b,
        "RSHIFT": lambda a, b: a >> b,
        "NOT": lambda a: 65535 - a,
        "=": lambda a: a
    }
    connections = {}

    for line in input_lines(INPUT_PATH):
        if m := re.match(r"(\w+) -> (\w+)", line):
            in_1, out = m.groups()
            connections[out] = ("=", in_1)
        elif m := re.match(r"([\w]+) ([A-Z]+) (\w+) -> (\w+)", line):
            in_1, op, in_2, out = m.groups()
            connections[out] = (op, in_1, in_2)
        elif m := re.match(r"NOT (\w+) -> (\w+)", line):
            in_1, out = m.groups()
            connections[out] = ("NOT", in_1)
        else:
            raise ValueError(f"Unknown operation: {line}")

    connections["b"] = ("=", "16076")

    @cache
    def get_result(target: str) -> int:
        if target.isdecimal():
            return int(target)

        operation, *values = connections[target]
        resolved_values = [get_result(v) for v in values]
        return operations[operation](*resolved_values)

    return get_result("a")


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
