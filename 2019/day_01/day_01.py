import math
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2019/day/1
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    with open("input.txt", "r") as file_handle:
        data = file_handle.read()

    numbers = []
    for line in data.strip().split("\n"):
        new_num = int(line.strip())
        numbers.append(new_num)

    result = 0
    for i in range(len(numbers)):
        a = math.floor(numbers[i] / 3) - 2
        result = result + a

    return result


def part_2() -> Union[int, str]:
    total_fuel = 0
    for mass in [int(n) for n in input_lines(_INPUT_PATH) if n != ""]:
        new_fuel = (mass // 3) - 2
        while new_fuel != 0:
            fuels_fuel = (new_fuel // 3) - 2
            total_fuel += new_fuel

            if fuels_fuel <= 0:
                new_fuel = 0
            else:
                new_fuel = fuels_fuel

    return total_fuel




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
