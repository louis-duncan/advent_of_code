import re
import time
from fractions import Fraction

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/13
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    games: list[dict[str, tuple[int, int]]] = []

    lines = list(input_lines(_INPUT_PATH))
    for i in range(0, len(lines), 4):
        block = " ".join(lines[i: i + 4])
        nums = [int(n) for n in re.findall(r"\d+", block)]
        games.append(
            {
                'a': (nums[0], nums[1]),
                'b': (nums[2], nums[3]),
                'prize': (nums[4], nums[5]),
            }
        )

    result = 0

    for game in games:
        adx, ady = game['a']
        bdx, bdy = game['b']
        tx, ty = game['prize']
        ak = ady / adx
        bk = bdy / bdx
        m = round((-ty + (bk * tx)) / (bk - ak), 5)

        if m % adx != 0:
            continue
        elif (tx - m) % bdx != 0:
            continue

        a_presses = m // adx
        b_pressed = (tx - m) // bdx
        result += a_presses * 3
        result += b_pressed

    return int(result)



def part_2() -> Union[int, str]:
    games: list[dict[str, tuple[int, int]]] = []
    c = 10000000000000

    lines = list(input_lines(_INPUT_PATH))
    for i in range(0, len(lines), 4):
        block = " ".join(lines[i: i + 4])
        nums = [int(n) for n in re.findall(r"\d+", block)]
        games.append(
            {
                'a': (nums[0], nums[1]),
                'b': (nums[2], nums[3]),
                'prize': (nums[4] + c, nums[5] + c),
            }
        )

    result = 0

    for game in games:
        adx, ady = game['a']
        bdx, bdy = game['b']
        tx, ty = game['prize']
        ak = Fraction(ady, adx)
        bk = Fraction(bdy, bdx)
        m = Fraction((-ty + (bk * tx)), (bk - ak))

        a_check = m % adx
        if a_check != 0 and a_check != adx:
            continue
        b_check = (tx - m) % bdx
        if b_check != 0 and b_check != bdx:
            continue

        a_presses = m / adx
        b_pressed = (tx - m) / bdx
        result += int(a_presses * 3)
        result += int(b_pressed)

    return int(result)


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
