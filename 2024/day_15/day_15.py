import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/15
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def get_contiguous_points(point: Point, direction: int, stop_value: str = "#") -> set[PointAgent]:
    points: set[Union[PointAgent, Point]] = {point}
    current_fronts: set[Point] = {point}
    while len(current_fronts):
        for _ in range(len(current_fronts)):
            current = current_fronts.pop()
            if current.value == stop_value:
                continue
            neighbours = current.get_neighbours(direction)
            if len(neighbours) == 0:
                continue
            points.add(neighbours[0])
            current_fronts.add(neighbours[0])
            if neighbours[0].value == "[" and direction not in (2, 6):
                extra = neighbours[0].get_neighbours(2)[0]
                points.add(extra)
                current_fronts.add(extra)
            elif neighbours[0].value == "]" and direction not in (2, 6):
                extra = neighbours[0].get_neighbours(6)[0]
                points.add(extra)
                current_fronts.add(extra)
    return points


def part_1() -> Union[int, str]:
    lines = list(input_lines(_INPUT_PATH))
    grid = PointGrid(lines[:lines.index("")], point_class=PointAgent)
    # noinspection PyTypeChecker
    bot: PointAgent = grid.find("@")[0]

    directions = "^ > v < "
    moves = [directions.index(c) for c in "".join(lines[lines.index(""):])]

    for d in moves:
        if bot.get_neighbours(d):
            to_move = get_contiguous_points(bot, d)
            if "#" not in [p.value for p in to_move]:
                for p in to_move:
                    p.move(d, 1)
        else:
            bot.move(d, 1)

    result = 0
    for p in grid.find("O"):
        result += 100 * p.y + p.x

    return result


def part_2() -> Union[int, str]:
    lines = list(input_lines(_INPUT_PATH))
    raw_text = "\n".join(lines[:lines.index("")])
    raw_text = raw_text.replace("#", "##")
    raw_text = raw_text.replace(".", "..")
    raw_text = raw_text.replace("@", "@.")
    raw_text = raw_text.replace("O", "[]")
    grid = PointGrid(raw_text.split("\n"), point_class=PointAgent)
    # noinspection PyTypeChecker
    bot: PointAgent = grid.find("@")[0]

    directions = "^ > v < "
    moves = [directions.index(c) for c in "".join(lines[lines.index(""):])]

    for d in moves:
        if bot.get_neighbours(d):
            to_move = get_contiguous_points(bot, d)
            if "#" not in [p.value for p in to_move]:
                for p in to_move:
                    p.move(d, 1)
        else:
            bot.move(d, 1)

    result = 0
    for p in grid.find("["):
        result += 100 * p.y + p.x

    return result


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
