import dataclasses
import itertools
import time
import random

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/9
"""

_INPUT_PATH = INPUT_PATH  # _TEST


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
        blocks[i] = 0

        while space_size > 0:
            if blocks[end_i] == 0:
                break
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


@dataclasses.dataclass
class File:
    pos: int
    size: int
    id: int

@dataclasses.dataclass
class Space:
    pos: int
    size: int


def part_2() -> Union[int, str]:
    values = [int(c) for c in raw_input(_INPUT_PATH).strip()]
    files: list[File] = []
    spaces: list[Space] = []
    pos = 0
    values.append(0)
    for file_num, i in enumerate(range(0, len(values), 2)):
        file_size = values[i]
        space_size = values[i + 1]
        if file_size > 0:
            files.append(File(pos, file_size, file_num))
            pos += file_size
        if space_size > 0:
            spaces.append(Space(pos, space_size))
            pos += space_size

    for file in list(reversed(files)):
        for space in spaces:
            if space.pos > file.pos:
                break
            elif space.size >= file.size:
                original_pos = file.pos
                file.pos = space.pos
                space.size -= file.size

                for i in range(len(spaces)):
                    assert spaces[i].pos != original_pos
                    if spaces[i].pos > original_pos:
                        spaces.insert(i, Space(original_pos, file.size))
                        break
                else:
                    spaces.append(Space(original_pos, file.size))

                if space.size > 0:
                    space.pos = space.pos + file.size
                else:
                    spaces.remove(space)
                break

    disk_hash = 0
    pos = 0
    for block in sorted(files + spaces, key=lambda b: b.pos):
        if isinstance(block, File):
            disk_hash += get_range_sum(pos, pos + block.size - 1) * block.id

        pos += block.size

    return disk_hash


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
