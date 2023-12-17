import re

from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2016/day/1
"""

compass = "NESW"


def part_1() -> Union[int, str]:
    pos = Point("N", 0, 0)
    instructions = raw_input("input.txt").strip().split(", ")
    for instruction in instructions:
        d = pos.value
        if instruction[0] == "L":
            new_d = compass[(compass.index(d) - 1) % len(compass)]
        else:
            new_d = compass[(compass.index(d) + 1) % len(compass)]
        pos.value = new_d

        for _ in range(int(instruction[1:])):
            if pos.value == "N":
                pos.y += 1
            elif pos.value == "E":
                pos.x += 1
            elif pos.value == "S":
                pos.y -= 1
            elif pos.value == "W":
                pos.x -= 1

    return abs(pos.x) + abs(pos.y)


def part_2() -> Union[int, str]:
    pos = Point("N", 0, 0)
    history: set[tuple[int, int]] = set()
    instructions = raw_input("input.txt").strip().split(", ")
    for instruction in instructions:
        d = pos.value
        if instruction[0] == "L":
            new_d = compass[(compass.index(d) - 1) % len(compass)]
        else:
            new_d = compass[(compass.index(d) + 1) % len(compass)]
        pos.value = new_d

        found = False
        for _ in range(int(instruction[1:])):
            if pos.value == "N":
                pos.y += 1
            elif pos.value == "E":
                pos.x += 1
            elif pos.value == "S":
                pos.y -= 1
            elif pos.value == "W":
                pos.x -= 1

            if pos.x_y in history:
                found = True
                break
            history.add(pos.x_y)
        if found:
            break

    return abs(pos.x) + abs(pos.y)


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
