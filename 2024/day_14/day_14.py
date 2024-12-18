import time
import re

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/14
"""

_INPUT_PATH = INPUT_PATH_TEST


def part_1() -> Union[int, str]:
    grid = AgentGrid()
    for line in input_lines(_INPUT_PATH):
        nums = [int(n) for n in re.findall(r"-?\d+", line)]
        agent = PointAgent(
            "#",
            x=nums[0], y=nums[1],
        )



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
