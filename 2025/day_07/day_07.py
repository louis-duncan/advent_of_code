import time
from typing import Union

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/7
"""

_INPUT_PATH = au.INPUT_PATH_TEST


def part_1() -> Union[int, str]:
    grid = au.LineGrid(au.input_lines(test=False))
    start_pos = grid.find("S")
    grid.set(start_pos[0], start_pos[1], "|")

    count = 0
    for x, y in grid.iterate_x_y():
        if y == 0:
            continue

        if grid.get(x, y - 1) == "|":
            if grid.get(x, y) == "^":
                grid.set(x - 1, y, "|")
                grid.set(x + 1, y, "|")
                count += 1
            else:
                grid.set(x, y, "|")

    return count


def part_2() -> Union[int, str]:
    grid = au.LineGrid(au.input_lines(test=False))
    grid.replace_all("S", 1)
    grid.replace_all(".", 0)

    for x, y in grid.iterate_x_y():
        if y == 0:
            continue

        if grid.get(x, y) == "^":
            val = grid.get(x, y - 1)
            if not val:
                continue
            new_left = grid.get(x-1, y) + val
            new_right = grid.get(x+1, y) + val
            grid.set(x-1, y, new_left)
            grid.set(x+1, y, new_right)
        else:
            val = grid.get(x, y - 1)
            if not val:
                continue
            if val == "^":
                continue
            new_val = grid.get(x, y) + val
            grid.set(x, y, new_val)

    return sum(grid.get_row(-1))


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
