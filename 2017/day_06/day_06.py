import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2017/day/6
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def redistribute(blocks: list[int]):
    pos = blocks.index(max(blocks))
    n = blocks[pos]
    blocks[pos] = 0
    for _ in range(n):
        pos += 1
        pos = pos % len(blocks)
        blocks[pos] += 1


def part_1() -> Union[int, str]:
    blocks: list[int] = [int(n) for n in raw_input(_INPUT_PATH).strip().split()]

    states: set[tuple[int, ...]] = {tuple(blocks),}
    done = False
    while not done:
        redistribute(blocks)
        new_state = tuple(blocks)
        if new_state in states:
            break
        else:
            states.add(new_state)

    return len(states)


def part_2() -> Union[int, str]:
    blocks: list[int] = [int(n) for n in raw_input(_INPUT_PATH).strip().split()]

    states: dict[tuple[int, ...], int] = {tuple(blocks): 0}
    new_state: tuple[int, ...] = tuple()
    done = False
    count = 0
    while not done:
        count += 1
        redistribute(blocks)
        new_state = tuple(blocks)
        if new_state in states:
            break
        else:
            states[new_state] = count

    return len(states) - states[new_state]


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
