import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/6
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    lines = list(input_lines(_INPUT_PATH))
    x_max = len(lines[0]) - 1
    y_max = len(lines) - 1
    grid = AgentGrid(lines)
    guard: Optional[PointAgent] = grid.find("^")
    guard.direction = 0
    assert guard is not None

    visited: set[tuple[int, int]] = set()
    while True:
        visited.add(guard.x_y)
        while guard.get_neighbours(guard.direction):
            guard.turn("R")
        guard.move("F", 1)
        if guard.x > x_max or guard.y > y_max:
            break

    return len(visited)


def part_2() -> Union[int, str]:
    lines = list(input_lines(_INPUT_PATH))
    x_max = len(lines[0]) - 1
    y_max = len(lines) - 1
    grid = AgentGrid(lines)
    guard: Optional[PointAgent] = grid.find("^")
    guard.direction = 0
    guard_start_x_y = guard.x_y
    assert guard is not None

    visited: set[tuple[int, int]] = set()
    while True:
        visited.add(guard.x_y)
        while guard.get_neighbours(guard.direction):
            guard.turn("R")
        guard.move("F", 1)
        if guard.x > x_max or guard.x < 0 or guard.y > y_max or guard.y < 0:
            break

    valid_obstructions: list[Point] = []
    for x, y in visited:
        if (x, y) == guard.x_y:
            continue

        # Reset
        grid.remove(guard)
        guard.x, guard.y = guard_start_x_y
        grid.add(guard)
        guard.direction = 0
        new = Point("O", x, y)
        grid.add(new)

        new_visited: set[tuple[int, int, int]] = set()
        while True:
            state = (guard.x, guard.y, guard.direction)
            if state in new_visited:
                valid_obstructions.append(new)
                break
            else:
                new_visited.add(state)

            if guard.get_neighbours(guard.direction):
                guard.turn("R")
            else:
                guard.move("F", 1)
                if guard.x > x_max or guard.x < 0 or guard.y > y_max or guard.y < 0:
                    break

        grid.remove(new)

    return len(valid_obstructions)


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
