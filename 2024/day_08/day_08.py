import itertools
import time
from fractions import Fraction

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/8
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    lines = list(input_lines(_INPUT_PATH))
    x_max = len(lines[0]) - 1
    y_max = len(lines) - 1
    antennas = PointGrid(lines)
    frequencies = set([a.value for a in antennas.points])

    antinodes: set[tuple[int, int]] = set()

    for f in frequencies:
        frequency_antennas = antennas.find(f)
        if len(frequency_antennas) < 2:
            continue
        for a, b in itertools.combinations(frequency_antennas, r=2):
            dx = a.x - b.x
            dy = a.y - b.y
            node_1 = (a.x + dx, a.y + dy)
            if  0 <= node_1[0] <= x_max and 0 <= node_1[1] <= y_max:
                antinodes.add(node_1)
            node_2 = (b.x - dx, b.y - dy)
            if  0 <= node_2[0] <= x_max and 0 <= node_2[1] <= y_max:
                antinodes.add(node_2)

    return len(antinodes)



def part_2() -> Union[int, str]:
    lines = list(input_lines(_INPUT_PATH))
    x_max = len(lines[0]) - 1
    y_max = len(lines) - 1
    antennas = PointGrid(lines)
    frequencies = set([a.value for a in antennas.points])

    antinodes: set[tuple[int, int]] = set()

    for f in frequencies:
        frequency_antennas = antennas.find(f)
        if len(frequency_antennas) < 2:
            continue
        a: Point
        b: Point
        for a, b in itertools.combinations(frequency_antennas, r=2):
            dx = a.x - b.x
            dy = a.y - b.y
            dx, dy = Fraction(dx, dy).as_integer_ratio()
            node = a.x_y
            antinodes.add(node)
            while True:
                node = (node[0] + dx, node[1] + dy)
                if 0 <= node[0] <= x_max and 0 <= node[1] <= y_max:
                    antinodes.add(node)
                else:
                    break
            node = a.x_y
            while True:
                node = (node[0] - dx, node[1] - dy)
                if 0 <= node[0] <= x_max and 0 <= node[1] <= y_max:
                    antinodes.add(node)
                else:
                    break

    return len(antinodes)


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
