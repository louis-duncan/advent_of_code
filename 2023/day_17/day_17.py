from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2023/day/17
"""


def part_1() -> Union[int, str]:
    grid = LineGrid(input_lines("test_input.txt"))
    



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
