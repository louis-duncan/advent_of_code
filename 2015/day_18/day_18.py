import itertools
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/18
"""

_INPUT_PATH = INPUT_PATH  # _TEST

null = object


def part_1() -> Union[int, str]:
    grid = LineGrid(input_lines(_INPUT_PATH))
    new_values = [["" for _ in range(grid.height)] for _ in range(grid.width)]
    # print(grid)

    for _ in range(100):
        for x, y in grid.iterate_x_y():
            neighbours: List[str] = []
            for dx, dy in ((i, j) for i in (-1, 0, 1) for j in (-1, 0, 1)):
                if dx == dy == 0:
                    continue
                try:
                    new = grid.get(x + dx, y + dy)
                except ValueError:
                    continue
                neighbours.append(new)

            value = grid.get(x, y)
            if value == "#":
                if neighbours.count("#") not in (2, 3):
                    value = "."
            else:
                if neighbours.count("#") == 3:
                    value = "#"
            new_values[x][y] = value

        for x, y in grid.iterate_x_y():
            grid.set(x, y, new_values[x][y])

        # print("--------------------")
        # print(grid)

    return sum((line.count("#") for line in grid.lines))


def part_2() -> Union[int, str]:
    grid = LineGrid(input_lines(_INPUT_PATH))
    new_values = [["" for _ in range(grid.height)] for _ in range(grid.width)]
    grid.set(0, 0, "#")
    grid.set(-1, 0, "#", wrap=True)
    grid.set(0, -1, "#", wrap=True)
    grid.set(-1, -1, "#", wrap=True)

    # print(grid)

    for _ in range(100):
        for x, y in grid.iterate_x_y():
            neighbours: List[str] = []
            for dx, dy in ((i, j) for i in (-1, 0, 1) for j in (-1, 0, 1)):
                if dx == dy == 0:
                    continue
                try:
                    new = grid.get(x + dx, y + dy)
                except ValueError:
                    continue
                neighbours.append(new)

            value = grid.get(x, y)
            if value == "#":
                if neighbours.count("#") not in (2, 3):
                    value = "."
            else:
                if neighbours.count("#") == 3:
                    value = "#"
            new_values[x][y] = value

        for x, y in grid.iterate_x_y():
            grid.set(x, y, new_values[x][y])

        grid.set(0, 0, "#")
        grid.set(-1, 0, "#", wrap=True)
        grid.set(0, -1, "#", wrap=True)
        grid.set(-1, -1, "#", wrap=True)

        # print("--------------------")
        # print(grid)

    return sum((line.count("#") for line in grid.lines))


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
