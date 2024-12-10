import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/10
"""

_INPUT_PATH = INPUT_PATH  # _TEST

def get_ends(point: Point) -> set[tuple[int, int]]:
    ends: set[tuple[int, int]] = set()
    for n_s in [point.get_neighbours(d) for d in "NESW"]:
        if len(n_s) == 1:
            n: Point = n_s[0]
        else:
            continue

        if n.value == (point.value + 1):
            if n.value == 9:
                ends.add(n.x_y)
            else:
                for e in get_ends(n):
                    ends.add(e)
    return ends


def get_count(point: Point) -> int:
    count = 0
    for n_s in [point.get_neighbours(d) for d in "NESW"]:
        if len(n_s) == 1:
            n: Point = n_s[0]
        else:
            continue

        if n.value == (point.value + 1):
            if n.value == 9:
                count += 1
            else:
                count += get_count(n)
    return count


def part_1() -> Union[int, str]:
    grid = PointGrid(input_lines(_INPUT_PATH))
    for p in grid.points:
        p.value = int(p.value)
    start_points = grid.find(0)
    score = 0
    for start in start_points:
        ends = get_ends(start)
        score += len(ends)
    return score

def part_2() -> Union[int, str]:
    grid = PointGrid(input_lines(_INPUT_PATH))
    for p in grid.points:
        p.value = int(p.value)
    start_points = grid.find(0)
    score = 0
    for start in start_points:
        score += get_count(start)
    return score


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
