import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2017/day/3
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def coord_from_value(value: int) -> tuple[int, int]:
    ring = 0
    start = 1
    end = 1
    width = 1
    while end < value:
        ring += 1
        width = (ring * 2) + 1
        start = (max(0, width - 2) ** 2) + 1
        end = width ** 2

    block_size = width - 1
    block_ends = (block_size, 2 * block_size, 3 * block_size, 4 * block_size)
    block_end_values = tuple([start + block_end - 1 for block_end in block_ends])
    start_x = ring
    start_y = -max(0, ring - 1)
    side_num = min([i for i in range(4) if value <= block_end_values[i]])

    if side_num == 0:
        x = start_x
        y = start_y + (block_size - (block_end_values[0] - value)) - 1
    elif side_num == 1:
        x = start_x - (block_size - (block_end_values[1] - value))
        y = start_y + block_ends[0] - 1
    elif side_num == 2:
        x = start_x - width + 1
        y = (start_y + block_size - 1) - (block_size - (block_end_values[2] - value))
    else:
        x = (start_x - block_size) + (block_size - (block_end_values[3] - value))
        y = start_y - 1

    return x, y


def part_1() -> Union[int, str]:
    target: int = int(raw_input(_INPUT_PATH).strip())
    x, y = coord_from_value(target)
    return manhattan_distance((0, 0), (x, y))



def part_2() -> Union[int, str]:
    target: int = int(raw_input(_INPUT_PATH).strip())

    grid = PointGrid()
    grid.add(Point(1, 0, 0))

    def gen_coords(start: int = 1):
        value = start
        while True:
            yield coord_from_value(value)
            value += 1

    for x, y in gen_coords(2):
        neighbours = grid.get_neighbours(x, y)
        total = sum([p.value for p in neighbours])
        if total > target:
            return total
        grid.add(Point(total, x, y))




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
