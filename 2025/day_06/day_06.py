import operator
import re
import time
from typing import Union, Any, Generator, Iterable

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/6
"""


def part_1() -> Union[int, str]:
    table = []
    for line in au.input_lines(test=False):
        table.append(
            re.findall(r"\d+|\*|\+", line)
        )
    cols = []
    for i in range(len(table[0])):
        cols.append([table[j][i] for j in range(len(table))])

    ops = {"*": operator.mul, "+": operator.add}

    total = 0
    for c in cols:
        reg = int(c[0])
        op = ops[c[-1]]
        for v in c[1:-1]:
            reg = op(reg, int(v))
        total += reg

    return total


def column_groups(columns: Iterable[list[Any]]) -> Generator[list[list[str]]]:
    group = []
    for col in columns:
        if all((c == " " for c in col)):
            yield group
            group = []
        else:
            group.append(col)
    yield group



def part_2() -> Union[int, str]:
    lines = [list(line) for line in au.raw_input(test=False).rstrip().split("\n")]
    grid = au.BasicGrid(data_rows=lines, default_value=" ")

    total = 0
    for group in column_groups(reversed(list(grid.columns))):
        values = []
        op_str = ""
        for col in group:
            values.append(int("".join(col[:-1])))
            if col[-1] in "+*":
                op_str = col[-1]
        op = {"*": operator.mul, "+": operator.add}[op_str]
        reg = values[0]
        for v in values[1:]:
            reg = op(reg, v)
        total += reg

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
