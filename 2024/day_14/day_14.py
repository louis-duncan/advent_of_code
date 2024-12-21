import math
import time
import re

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/14
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    width = 101
    height = 103
    grid = AgentGrid(None)
    robot: VelocityPoint
    for line in input_lines(_INPUT_PATH):
        nums = [int(n) for n in re.findall(r"-?\d+", line)]
        robot = VelocityPoint(
            "#",
            x=nums[0], y=nums[1],
            vx=nums[2], vy=nums[3]
        )
        grid.add(robot)

    for _ in range(100):
        for robot in grid.points:
            robot.update()
            out_of_bounds = False
            new_x, new_y = robot.x_y
            if new_x >= width or new_x < 0:
                out_of_bounds = True
                new_x = new_x % width
            if new_y >= height or new_y < 0:
                out_of_bounds = True
                new_y = new_y % height
            if out_of_bounds:
                robot.move_to(new_x, new_y)

    quad_one = grid.get_region(
        (0, 0), ((width // 2) - 1, (height // 2) - 1)
    )
    quad_two = grid.get_region(
        ((width // 2) + 1, 0), (width - 1, (height // 2) - 1)
    )
    quad_three = grid.get_region(
        (0, (height // 2) + 1), ((width // 2) - 1, height - 1),
    )
    quad_four = grid.get_region(
        ((width // 2) + 1, (height // 2) + 1), (width - 1, height - 1),
    )

    return len(quad_one) * len(quad_two) * len(quad_three) * len(quad_four)


def part_2() -> Union[int, str]:
    width = 101
    height = 103
    grid = AgentGrid(None)
    robot: VelocityPoint
    for line in input_lines(_INPUT_PATH):
        nums = [int(n) for n in re.findall(r"-?\d+", line)]
        robot = VelocityPoint(
            "#",
            x=nums[0], y=nums[1],
            vx=nums[2], vy=nums[3]
        )
        grid.add(robot)

    n = 0
    occupied_points = set()
    num_robots = len(grid.points)
    while True:
        occupied_points.clear()
        for robot in grid.points:
            robot.update()
            out_of_bounds = False
            new_x, new_y = robot.x_y
            if new_x >= width or new_x < 0:
                out_of_bounds = True
                new_x = new_x % width
            if new_y >= height or new_y < 0:
                out_of_bounds = True
                new_y = new_y % height
            if out_of_bounds:
                robot.move_to(new_x, new_y)
            occupied_points.add((new_x, new_y))
        n += 1

        if len(occupied_points) == num_robots:
            print(str(grid))
            print(n)
            try:
                input()
            except KeyboardInterrupt:
                break

    return n


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
