import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/5
"""


def part_1() -> Union[int, str]:
    def is_nice(text: str) -> bool:
        bad_strings = ["ab", "cd", "pq", "xy"]
        vowels = "aeiou"
        for bad_string in bad_strings:
            if bad_string in text:
                return False
        has_repeat = False
        vowel_count = 0
        prev_char = ""
        for char in text:
            if char in vowels:
                vowel_count += 1
            if char == prev_char:
                has_repeat = True
            if vowel_count >= 3 and has_repeat:
                return True
            else:
                prev_char = char
        return False
    words = input_lines("input.txt")
    return sum([is_nice(word) for word in words])


def part_2() -> Union[int, str]:
    def is_nice(text: str) -> bool:
        if not re.match(r"\b.*(\w{2}).*\1.*\b", text):
            return False
        if not re.match(r"\b.*(\w).\1.*\b", text):
            return False
        return True

    words = input_lines("input.txt")
    return sum([is_nice(word) for word in words])


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
