import re
from dataclasses import dataclass
from functools import cache
from math import prod

from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2023/day/15
"""


@cache
def string_hash(string: str) -> int:
    """
    Start with a current value of 0. Then, for each character in the string starting from the beginning:
        - Determine the ASCII code for the current character of the string.
        - Increase the current value by the ASCII code you just determined.
        - Set the current value to itself multiplied by 17.
        - Set the current value to the remainder of dividing itself by 256.
    After following these steps for each character in the string in order, the current value is the output of the HASH algorithm.
    """
    value = 0
    for c in string:
        value += ord(c)
        value *= 17
        value %= 256
    return value


@dataclass
class Lens:
    label: str
    focal_length: int


def part_1() -> Union[int, str]:
    instructions: list[str] = raw_input("input.txt").strip().split(",")
    return sum([string_hash(inst) for inst in instructions])


def part_2() -> Union[int, str]:
    instructions: list[str] = raw_input("input.txt").strip().split(",")

    boxes: list[list[Lens]] = [[] for _ in range(256)]

    for instruction in instructions:
        label, op, value = re.match(r"(\w+)([-=])(\d+)?", instruction).groups()
        if value:
            value = int(value)

        box_i = string_hash(label)

        if op == "-":
            """
            If the operation character is a dash (-), go to the relevant box and remove the lens with the given label if 
            it is present in the box. Then, move any remaining lenses as far forward in the box as they can go without 
            changing their order, filling any space made by removing the indicated lens. (If no lens in that box has the 
            given label, nothing happens.)
            """
            for i in range(len(boxes[box_i])):
                if boxes[box_i][i].label == label:
                    boxes[box_i].pop(i)
                    break
        else:
            """
            If the operation character is an equals sign (=), it will be followed by a number indicating the focal length 
            of the lens that needs to go into the relevant box; be sure to use the label maker to mark the lens with the 
            label given in the beginning of the step so you can find it later. There are two possible situations:
                - If there is already a lens in the box with the same label, replace the old lens with the new lens: remove 
                  the old lens and put the new lens in its place, not moving any other lenses in the box.
                - If there is not already a lens in the box with the same label, add the lens to the box immediately behind 
                  any lenses already in the box. Don't move any of the other lenses when you do this. If there aren't any 
                  lenses in the box, the new lens goes all the way to the front of the box.
            """
            for i in range(len(boxes[box_i])):
                if boxes[box_i][i].label == label:
                    boxes[box_i][i] = Lens(label, value)
                    break
            else:
                boxes[box_i].append(Lens(label, value))

    total = 0
    for box_i, box in enumerate(boxes):
        for lens_i, lens in enumerate(box):
            total += prod([box_i + 1, lens_i + 1, lens.focal_length])

    return total


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
