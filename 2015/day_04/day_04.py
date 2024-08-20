import random
import time
from hashlib import md5

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/4
"""


def part_1() -> Union[int, str]:
    secret = raw_input(INPUT_PATH)
    max_num = 9999999
    prev = 0
    same_count = 0
    while same_count < 3:
        num = random.randint(0, max_num)
        hash_value = md5((secret + str(num)).encode()).hexdigest()
        if hash_value.startswith("00000"):
            if num == prev:
                same_count += 1
            else:
                same_count = 0
            max_num = num
            prev = num
            print(num)
    return max_num


def part_2() -> Union[int, str]:
    secret = raw_input(INPUT_PATH)
    max_num = 9999999
    prev = 0
    same_count = 0
    while same_count < 3:
        num = random.randint(0, max_num)
        hash_value = md5((secret + str(num)).encode()).hexdigest()
        if hash_value.startswith("000000"):
            if num == prev:
                same_count += 1
            else:
                same_count = 0
            max_num = num
            prev = num
            print(num)
    return max_num


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
