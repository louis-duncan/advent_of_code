import time
from typing import Union

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/1
"""

_INPUT_PATH = au.INPUT_PATH #  _TEST


def part_1() -> Union[int, str]:
    input_lines  = au.input_lines(_INPUT_PATH)

    pos = 50
    count = 0

    for line in input_lines:
        direction = line[0]
        val = int(line[1:].strip())
        if direction == "R":
            pos += val
        else:
            pos -= val

        if pos % 100 == 0:
            count +=1

    return count


def part_2() -> Union[int, str]:
    input_lines = au.input_lines(_INPUT_PATH)

    pos = 50
    count = 0
    prev_seg = 0
    was_on_zero = False

    for line in input_lines:
        direction = line[0]
        val = int(line[1:].strip())

        for _ in range(val):
            if direction == "R":
                pos += 1
            else:
                pos -= 1

            if pos % 100 == 0:
                count += 1

        """
        if direction == "R":
            pos += val
        else:
            pos -= val

        cur_seg = pos // 100
        on_zero = pos % 100 == 0

        if (cur_seg == prev_seg) and (on_zero and not was_on_zero):
            count += 1
        else:
            count += abs(cur_seg - prev_seg) - int(was_on_zero)

        was_on_zero = on_zero
        prev_seg = cur_seg
        """

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
