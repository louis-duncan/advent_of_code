import itertools
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/9
"""

_INPUT_PATH = INPUT_PATH_TEST


def get_range_sum(a: int, b: int) -> int:
    sum_b = int((b * (b + 1)) / 2)
    sum_a = int(((a - 1) * a) / 2)
    return sum_b - sum_a


def part_1() -> Union[int, str]:
    values = [int(c) for c in raw_input(_INPUT_PATH).strip()]
    blocks: list[int] = []
    spaces: list[int] = []
    for i in range(0, len(values), 2):
        blocks.append(values[i])
        try:
            spaces.append(values[i + 1])
        except IndexError:
            pass
    spaces.append(0)

    pos = 0
    checksum = 0
    end_i = len(blocks) - 1
    for i, (block_size, space_size) in enumerate(zip(blocks, spaces)):
        if block_size == 0:
            continue
        m = get_range_sum(pos, pos + block_size - 1)
        checksum += i * m
        pos += block_size

        while space_size > 0:
            if space_size >= blocks[end_i]:
                assert blocks[end_i] > 0
                m = get_range_sum(pos, pos + blocks[end_i] - 1)
                checksum += end_i * m
                space_size -= blocks[end_i]
                pos += blocks[end_i]
                blocks[end_i] = 0
                end_i -= 1
            else:
                assert blocks[end_i] > 0
                m = get_range_sum(pos, pos + space_size - 1)
                checksum += end_i * m
                pos += space_size
                blocks[end_i] -= space_size
                space_size = 0
    return checksum





def part_2() -> Union[int, str]:
    ...


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
