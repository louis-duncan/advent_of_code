import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/11
"""

_INPUT_PATH = INPUT_PATH # _TEST


def run_blinks(num_blinks: int) -> int:
    stones: dict[int, int] = {}
    for n_str in raw_input(_INPUT_PATH).strip().split():
        n = int(n_str)
        stones[n] = stones.get(n, 0) + 1

    for _ in range(num_blinks):
        new_stones = {}
        for s in stones:
            if s == 0:
                new_stones[1] = new_stones.get(1, 0) + stones[s]
            elif len(str(s)) % 2 == 0:
                s_str = str(s)
                s_str_len = len(s_str)
                n_l = int(s_str[:s_str_len // 2])
                n_r = int(s_str[s_str_len // 2:])
                new_stones[n_l] = new_stones.get(n_l, 0) + stones[s]
                new_stones[n_r] = new_stones.get(n_r, 0) + stones[s]
            else:
                n = s * 2024
                new_stones[n] = new_stones.get(n, 0) + stones[s]
        stones = new_stones

    return sum(stones.values())


def part_1() -> Union[int, str]:
    return run_blinks(25)


def part_2() -> Union[int, str]:
    return run_blinks(75)


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
