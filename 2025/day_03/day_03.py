import itertools
import time
from idlelib.help import copy_strip
from typing import Union

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/3
"""

_INPUT_PATH = au.INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    lines = au.input_lines(_INPUT_PATH)

    jolts_sum = 0

    for bank in lines:
        biggest = 0
        for comb in itertools.combinations(bank, 2):
            v = int("".join(comb))
            if v > biggest:
                biggest = v
            if biggest == 99:
                break

        jolts_sum += biggest

    return jolts_sum

"""
def search_bank(consider: tuple[int, ...], against: tuple[int, ...]) -> tuple[int, ...] | None:
    if len(against) > len(consider):
        return tuple()

    resp = tuple()
    for i in range(len(consider)):
"""

def get_leftmost_biggest_index(consider: tuple[int, ...]) -> int:
    n = max(consider)
    return consider.index(n)


def part_2() -> Union[int, str]:
    lines = au.input_lines(_INPUT_PATH)

    jolts_sum = 0

    for line in lines:
        values = tuple(int(c) for c in line)
        indexes = []
        for i in range(12):
            start = 0 if not indexes else indexes[-1] + 1
            end = -12 + (i + 1)
            consider = values[start: end if end else None]
            indexes.append(
                get_leftmost_biggest_index(
                    consider
                ) + start
            )
        jolts_sum += int("".join([str(values[j]) for j in indexes]))

    return jolts_sum


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
