import time
from typing import Union

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/4
"""

_INPUT_PATH = au.INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    grid = au.PointGrid(au.input_lines(_INPUT_PATH))

    count = 0
    for p in grid.points:
        if len(p.get_neighbours()) < 4:
            count += 1
    return count


def part_2() -> Union[int, str]:
    grid = au.PointGrid(au.input_lines(_INPUT_PATH))

    total_removed = 0
    keep_going = True
    while keep_going:
        keep_going = False
        to_remove = []
        for p in grid.points:
            if len(p.get_neighbours()) < 4:
                to_remove.append(p)
        if to_remove:
            keep_going = True
            total_removed += len(to_remove)
        for p in to_remove:
            grid.remove(p)

    return total_removed


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
