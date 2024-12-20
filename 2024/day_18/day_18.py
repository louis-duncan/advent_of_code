import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/18
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    width, height = 71, 71
    grid = LineGrid(["." * width] * height)
    for i, line in enumerate(input_lines(_INPUT_PATH)):
        if i == 1024:
            break
        x, y = [int(n) for n in re.findall(r"\d+", line)]
        grid.set(x, y, "#")

    path = grid.get_shortest_path((0, 0), (70, 70), {"."})
    for p in path:
        grid.set(p[0], p[1], "O")

    return len(path) - 1


def part_2() -> Union[int, str]:
    width, height = 71, 71

    coords: list[tuple[int, int]] = []
    for line in input_lines(_INPUT_PATH):
        x, y = [int(n) for n in re.findall(r"\d+", line)]
        coords.append((x, y))

    low = 1024
    high = len(coords) - 1
    while True:
        num = ((high - low) // 2) + low
        grid = LineGrid(["." * width] * height)
        for coord in coords[:num]:
            grid.set(coord[0], coord[1], "#")
        try:
            _ = grid.get_shortest_path((0, 0), (width - 1, height - 1), {"."})
            low = num
        except ValueError:
            high = num

        if low == high or low == high - 1:
            result = coords[num]
            return f"{result[0]},{result[1]}"


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
