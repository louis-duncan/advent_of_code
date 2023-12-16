from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2015/day/1
"""


def part_1() -> Union[int, str]:
    chars = raw_input("input.txt")
    ups = chars.count("(")
    downs = chars.count(")")
    return ups - downs


def part_2() -> Union[int, str]:
    chars = raw_input("input.txt")
    pos = 0
    i = 0
    for i, char in enumerate(chars):
        if char == "(":
            pos += 1
        else:
            pos -= 1
        if pos == -1:
            break
    return i + 1


if __name__ == "__main__":
    part_1_answer = part_1()
    if part_1_answer is not None:
        print("Part 1:", part_1())
        pyperclip.copy(part_1_answer)

    part_2_answer = part_2()
    if part_2_answer is not None:
        print()
        print("Part 2:", part_2())
        pyperclip.copy(part_2_answer)
