import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/4
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def get_coords(x: int, y: int, d: int, n: int) -> list[tuple[int, int]]:
    if d == 0:
        dx, dy = 0, -1
    elif d == 1:
        dx, dy = 1, -1
    elif d == 2:
        dx, dy = 1, 0
    elif d == 3:
        dx, dy = 1, 1
    elif d == 4:
        dx, dy = 0, 1
    elif d == 5:
        dx, dy = -1, 1
    elif d == 6:
        dx, dy = -1, 0
    elif d == 7:
        dx, dy = -1, -1
    else:
        raise ValueError("Invalid direction")

    return [(x + (i * dx), y + (i * dy)) for i in range(n)]


def part_1() -> Union[int, str]:
    grid = LineGrid(input_lines(_INPUT_PATH))

    count = 0
    target = "XMAS"
    target_len = len(target)
    for x, y in grid.iterate_x_y():
        for d in range(8):
            for coord, t in zip(get_coords(x, y, d, target_len), target):
                try:
                    if grid.get(*coord) != t:
                        break
                except ValueError:
                    break
            else:
                count += 1

    return count


def part_2() -> Union[int, str]:
    grid = LineGrid(input_lines(_INPUT_PATH))

    count = 0
    for x, y in grid.iterate_x_y():
        if grid.get(x, y) == "A":
            try:
                corners = (grid.get(x + 1, y - 1) +
                           grid.get(x + 1, y + 1) +
                           grid.get(x - 1, y + 1) +
                           grid.get(x - 1, y - 1))
                if corners.count("M") == 2:
                    if corners.count("S") == 2:
                        if corners[0] != corners[2] and corners[1] != corners[3]:
                            count += 1
            except ValueError:
                pass
    return count


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
