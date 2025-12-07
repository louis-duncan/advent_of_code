import dataclasses
import time
from multiprocessing.managers import Value
from typing import Union

import pyperclip

import aoc_utils as au
from aoc_utils import input_lines, raw_input

"""
https://adventofcode.com/2025/day/5
"""

_INPUT_PATH = au.INPUT_PATH  # _TEST


@dataclasses.dataclass
class Range:
    start: int
    end: int

    @classmethod
    def from_line(cls, line: str) -> 'Range':
        s1, s2 = line.strip().split("-")
        return cls(int(s1), int(s2))

    def __add__(self, other: 'Range') -> 'Range':
        if self.start in other or other.start in self or other.end == self.start - 1 or self.end == other.start - 1:
            return Range(min(self.start, other.start), max(self.end, other.end))
        else:
            raise ValueError("Cannot add non-overlapping/non-sequential ranges")

    def __contains__(self, item: int) -> bool:
        return self.start <= item <= self.end


def part_1() -> Union[int, str]:
    ranges_raw, ingredients_raw = raw_input(_INPUT_PATH).split("\n\n")
    ranges_lines = ranges_raw.strip().split("\n")
    ingredients_lines = ingredients_raw.strip().split("\n")

    ranges = [Range.from_line(l) for l in ranges_lines]
    ingredients = [int(v) for v in ingredients_lines]

    keep_going = True
    while keep_going:
        keep_going = False
        to_merge: list[tuple[Range, Range]] = []
        for i in range(len(ranges)):
            for j in range(i + 1, len(ranges)):
                if ranges[i].start in ranges[j] or ranges[j].start in ranges[i]:
                    to_merge.append((ranges[i], ranges[j]))

        if to_merge:
            keep_going = True

        for r1, r2 in to_merge:
            try:
                ranges.remove(r1)
            except ValueError:
                pass
            try:
                ranges.remove(r2)
            except ValueError:
                pass

            ranges.append(r1 + r2)

    count = 0
    for ingredient in ingredients:
        for r in ranges:
            if ingredient in r:
                count += 1
                break
    return count


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
