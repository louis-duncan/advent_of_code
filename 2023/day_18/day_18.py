from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2023/day/18
"""


def part_1() -> Union[int, str]:
    holes = PointCloud(["#"])
    digger = PointAgent("", 0, 0)

    for line in input_lines("input.txt"):
        direction, distance, colour = line.split(" ")
        direction = check_direction(direction)
        distance = int(distance)
        colour = colour.strip("()")

        for _ in range(distance):
            digger.move(direction, 1)
            holes.add(Point("#", digger.x, digger.y))

    grid = LineGrid(str(holes).split("\n"))
    with open("out_pre.txt", "w") as fh:
        fh.write(str(grid))
    filled = grid.flood_fill("*", 0, 0)
    with open("out_post.txt", "w") as fh:
        fh.write(str(grid))

    area = (grid.width * grid.height) - filled

    return area


def part_2() -> Union[int, str]:
    ...


if __name__ == "__main__":
    part_1_answer = part_1()
    if part_1_answer is not None:
        print("Part 1:", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    part_2_answer = part_2()
    if part_2_answer is not None:
        print("Part 2:", part_2_answer)
        pyperclip.copy(part_2_answer)
