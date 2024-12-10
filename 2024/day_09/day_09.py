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
    id: int
    size: int
    _index: int

@dataclasses.dataclass
class Space:
    size: int
    _index: int


def part_2() -> Union[int, str]:
    values = [int(c) for c in raw_input(_INPUT_PATH).strip()]
    block_map: list[Union[File, Space]] = []
    values.append(0)
    for block_num, i in enumerate(range(0, len(values), 2)):
        block_size = values[i]
        space_size = values[i+1]
        if block_size > 0:
            block_map.append(File(block_num, block_size, block_num))
        if space_size > 0:
            block_map.append(Space(space_size, block_num))

    file_to_move: File
    space_to_fill: Space
    biggest_space = max((b.size for b in block_map if isinstance(b, Space)))
    for file_to_move in [b for b in reversed(block_map) if isinstance(b, File)]:
        if file_to_move.size > biggest_space:
            print("skip")
            continue
        i = block_map.index(file_to_move)
        for space_to_fill in (b for b in block_map if isinstance(b, Space)):
            j = block_map.index(space_to_fill)
            if j > i:
                break
            if space_to_fill.size >= file_to_move.size:
                block_map.remove(file_to_move)
                block_map.insert(i, Space(file_to_move.size, _index=random.randint(10000, 99999)))
                block_map.insert(j, file_to_move)
                space_to_fill.size -= file_to_move.size
                if space_to_fill.size == 0:
                    block_map.remove(space_to_fill)
                biggest_space = 0
                for k in range(len(block_map)):
                    if k >= i:
                        break
                    elif isinstance(block_map[k], Space) and block_map[k].size > biggest_space:
                        biggest_space = block_map[k].size
                break

    disk_hash = 0
    pos = 0
    for block in block_map:
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
