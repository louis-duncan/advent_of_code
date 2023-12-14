import math

from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2023/day/13
"""


def check_reflection(left: list[int], right: list[int]):
    for l, r in zip(reversed(left), right):
        if l != r:
            return False
    return True


def find_reflection_p1(values: list[int]) -> Optional[int]:
    start_stops_to_try: list[tuple[int, int, int]] = []

    if values[0] in values[1:]:
        start_stops_to_try.append((len(values) - 1, 0, -1))
    if values[-1] in values[:-1]:
        start_stops_to_try.append((0, len(values) - 1, 1))

    for start, stop, step in start_stops_to_try:
        for i in range(start, stop, step):
            if values[stop] == values[i]:
                if stop == 0:
                    mid = (i // 2) + 1
                else:
                    mid = i + ((stop - i) // 2) + 1
                left = values[:mid]
                right = values[mid:]
                if check_reflection(left, right):
                    return mid

    return None


def find_reflection_p2(hashes: list[int], counts: list[int]):
    ...


def part_1() -> Union[int, str]:
    total = 0
    for group in grouped_input_lines("input.txt"):
        grid = LineGrid(group)

        row_hashes = [hash(tuple(row)) for row in grid.rows]
        mid = find_reflection_p1(row_hashes)
        if mid is not None:
            total += mid * 100
            continue

        col_hashes = [hash(tuple(col)) for col in grid.columns]
        mid = find_reflection_p1(col_hashes)
        if mid is None:
            raise ValueError(f"No reflection...\n{grid}")
        total += mid

    return total


def part_2() -> Union[int, str]:
    ...


if __name__ == "__main__":
    part_1_answer = part_1()
    if part_1_answer is not None:
        print("Part 1:", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    part_2_answer = part_2()
    if part_2_answer is not None:
        print("Part 2:", part_2_answer)
        pyperclip.copy(part_2_answer)
