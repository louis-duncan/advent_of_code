import time
from functools import cached_property
from typing import Union

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/12
"""

_INPUT_PATH = au.INPUT_PATH_TEST


class Shape:
    collision_cache: dict[tuple['Shape', 'Shape', au.Vector], bool] = {}

    def __init__(self, shape_num: int, definition: str, pos: au.Point):
        self.shape_num = shape_num
        self.definition = definition
        self.pos = pos
        self._points: set[au.Vector] = set()

        lines = [l.strip() for l in self.definition.split("\n")]
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "#":
                    self._points.add(au.Vector(x, y))

    @property
    def points (self) -> set[au.Point]:
        return set(self.pos + p for p in self._points)

    def rotated(self) -> 'Shape':
        ...

    def __hash__(self):
        return hash(self.definition)



def part_1() -> Union[int, str]:
    ...


def part_2() -> Union[int, str]:
    ...


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
