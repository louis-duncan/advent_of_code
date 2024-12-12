import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/12
"""

_INPUT_PATH = INPUT_PATH # _TEST


def build_region(root: Point, grid: PointGrid) -> PointGrid:
    found_points: set[Point] = {root}
    to_search: list[Point] = [root]
    while to_search:
        subject = to_search.pop()
        for n in subject.get_neighbours([0, 2, 4, 6]):
            if n.value == root.value and n not in found_points:
                found_points.add(n)
                to_search.append(n)
    new_region = PointGrid()
    for p in found_points:
        grid.remove(p)
        new_region.add(p)
    return new_region


def get_perimeter(region: PointGrid) -> int:
    count = 0
    for p in region.points:
        count += 4 - len(p.get_neighbours([0, 2, 4, 6]))
    return count


def get_sides(region: PointGrid) -> int:
    num_corners = 0
    for p in region.y_x_sorted:
        ns: dict[str, Optional[Point]] = {}
        for d in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
            found = p.get_neighbours(d)
            if found:
                ns[d] = found[0]
            else:
                ns[d] = None

        if ns["N"] and ns["E"] and not ns["NE"]:
            num_corners += 1
        if ns["E"] and ns["S"] and not ns["SE"]:
            num_corners += 1
        if ns["S"] and ns["W"] and not ns["SW"]:
            num_corners += 1
        if ns["W"] and ns["N"] and not ns["NW"]:
            num_corners += 1
        if not (ns["N"] or ns["E"]):
            num_corners += 1
        if not (ns["E"] or ns["S"]):
            num_corners += 1
        if not (ns["S"] or ns["W"]):
            num_corners += 1
        if not (ns["W"] or ns["N"]):
            num_corners += 1

    return num_corners


def part_1() -> Union[int, str]:
    regions: list[PointGrid] = []

    garden = PointGrid(input_lines(_INPUT_PATH))

    while len(garden.points):
        new_region = build_region(garden.x_y_sorted[0], garden)
        regions.append(new_region)

    result = 0
    for region in regions:
        area = len(region.points)
        perimeter = get_perimeter(region)
        result += area * perimeter
    return result


def part_2() -> Union[int, str]:
    regions: list[PointGrid] = []

    garden = PointGrid(input_lines(_INPUT_PATH))

    while len(garden.points):
        new_region = build_region(garden.x_y_sorted[0], garden)
        regions.append(new_region)

    result = 0
    for region in regions:
        area = len(region.points)
        sides = get_sides(region)
        result += area * sides
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
