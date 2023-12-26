from functools import cache
import time

from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2023/day/22
"""

class Block(Point3Group):
    def __init__(self, p1: Point3, p2: Point3, cloud: Point3Cloud):
        super().__init__(
            p1=p1,
            p2=p2,
            cloud=cloud
        )
        self.supporting: list[Block] = []
        self.supported_by: list[Block] = []


@cache
def get_above(block: Block) -> set[Block]:
    above: set[Block] = set()
    for a in block.supporting:
        above.add(a)
        above.update(get_above(a))
    return above


@cache
def get_stack() -> list[Block]:
    point_cloud = Point3Cloud()
    point_blocks: list[Block] = []

    for line in input_lines("input.txt"):
        start_str, end_str = line.split("~")
        sx, sy, sz = start_str.split(",")
        start = (int(sx), int(sy), int(sz))
        ex, ey, ez = end_str.split(",")
        end = (int(ex), int(ey), int(ez))
        new_block = Block(
            p1=Point3(start[0], start[1], start[2]),
            p2=Point3(end[0], end[1], end[2]),
            cloud=point_cloud,
        )
        point_blocks.append(new_block)

    dropped: set[Point3Group] = set()
    for block in sorted(point_blocks, key=lambda b: b.min_z):
        if block not in dropped:
            done = False
            while not done:
                if (block.min_z == 1) or (len(block.get_neighbours((0, 0, -1))) > 0):
                    dropped.add(block)
                    done = True
                else:
                    block.move(dz=-1)

    for i, block in enumerate(point_blocks):
        block.supporting = block.get_neighbours((0, 0, 1))
        block.supported_by = block.get_neighbours((0, 0, -1))

    return point_blocks


def part_1() -> Union[int, str]:
    point_blocks: list[Point3Group] = get_stack()

    removable_blocks: list[Point3Group] = []
    for block in point_blocks:
        can_remove = True
        supporting: list[Point3Group] = block.get_neighbours((0, 0, 1))
        for n in supporting:
            if len(n.get_neighbours((0, 0, -1))) == 1:
                can_remove = False
                break
        if can_remove:
            removable_blocks.append(block)

    unmovable: set[Point3Group] = set()
    for block in point_blocks:
        below = block.get_neighbours((0, 0, -1))
        if len(below) == 1:
            unmovable.add(below[0])
    removable_2: set[Point3Group] = set(point_blocks).difference(unmovable)

    return len(removable_blocks)


def part_2() -> Union[int, str]:
    point_blocks: list[Block] = get_stack()

    count = 0
    for block in point_blocks:
        all_above = get_above(block)
        remaining = all_above.copy()
        for a in sorted(all_above, key=lambda b: b.min_z, reverse=False):
            if a not in remaining:
                continue
            elif len(remaining) == 0:
                break

            for s in a.supported_by:
                if (s not in all_above) and (s is not block):
                    remaining.remove(a)
                    remaining.difference_update(get_above(a))
                    break

        count += len(remaining)
    return count


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
