import re
from functools import cache

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


def part_1() -> Union[int, str]:
    instructions: list[str] = raw_input("input.txt").strip().split(",")
    return sum([string_hash(inst) for inst in instructions])


def part_2() -> Union[int, str]:
    instructions: list[str] = raw_input("input.txt").strip().split(",")

    boxes =     

    for instruction in instructions:
        label, op, value = re.match(r"(\w+)([-=])(\d+)?", instruction).groups()
        if value:
            value = int(value)




def find_clash():
    import random

    alph = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    results = {}
    while True:
        new_str = "".join(random.choices(alph, k=3))
        new_val = string_hash(new_str)
        if new_val in results:
            print(new_str, results[new_val], new_val)
            break
        else:
            results[new_val] = new_str


if __name__ == "__main__":
    find_clash()
    exit()

    part_1_answer = part_1()
    if part_1_answer is not None:
        print("Part 1:", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    part_2_answer = part_2()
    if part_2_answer is not None:
        print("Part 2:", part_2_answer)
        pyperclip.copy(part_2_answer)
