import dataclasses
import functools
import heapq
import itertools
import time
from math import inf
from typing import Set, Union, Optional, List, Generator

import colour
import pyperclip

from aoc_utils import INPUT_PATH_TEST, manhattan_distance, reconstruct_path, LineGrid, input_lines, get_direction, \
    INPUT_PATH

"""
https://adventofcode.com/2024/day/16
"""

_INPUT_PATH = INPUT_PATH  # _TEST


class RaceingGrid(LineGrid):
    def get_shortest_race_path(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            passable_values: Set[Union[str, int]],
    ) -> Generator[Optional[list[tuple[int, int]]], None, None]:
        @dataclasses.dataclass(order=True)
        class PrioritizedPoint:
            priority: int
            item: tuple[int, int] = dataclasses.field(compare=False)

        h = functools.partial(manhattan_distance, p2=end)

        open_set: List[PrioritizedPoint] = []
        heapq.heapify(open_set)
        heapq.heappush(open_set, PrioritizedPoint(0, start))
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score: dict[tuple[int, int], int] = {
            start: 0
        }
        f_score: dict[tuple[int, int], int] = {
            start: h(start)
        }
        while open_set:
            current: tuple[int, int] = heapq.heappop(open_set).item
            if current == end:
                yield reconstruct_path(came_from, current)

            for n in (self.get_neighbour_coord(*current, d) for d in (0, 2, 4, 6)):
                if not self.is_pos_in_bounds(*n):
                    continue
                elif self.get(*n) not in passable_values:
                    continue

                direction_facing = get_direction(
                    came_from.get(current, (current[0] - 1, current[1])),
                    current
                )
                direction_to_next = get_direction(
                    current,
                    n
                )
                cost = 1
                if ((direction_facing + 1) % 4 == direction_to_next) or ((direction_facing - 1) % 4 == direction_to_next):
                    cost += 1000

                # 1 here would be the edge weight between current and neighbour
                tentative_g_score = g_score.get(current, inf) + cost
                if tentative_g_score < g_score.get(n, inf):
                    came_from[n] = current
                    g_score[n] = tentative_g_score
                    f_score[n] = tentative_g_score + h(n)
                    if n not in open_set:
                        heapq.heappush(open_set, PrioritizedPoint(f_score[n], n))


def part_1() -> Union[int, str]:
    grid = RaceingGrid(input_lines(_INPUT_PATH))
    shortest_path = grid.get_shortest_race_path(
        start=grid.find("S"),
        end=grid.find("E"),
        passable_values=set(".SE")
    ).__next__()
    if shortest_path is None:
        raise ValueError("No path")
    pretty(grid, highlight_path=shortest_path)
    direction = 1
    score = 0
    for p1, p2 in itertools.pairwise(shortest_path):
        new_direction = get_direction(p1, p2)
        if new_direction != direction:
            score += 1000
        score += 1
        direction = new_direction
    return score


def part_2() -> Union[int, str]:
    grid = RaceingGrid(input_lines(_INPUT_PATH))
    paths = list(grid.get_shortest_race_path(
        start=grid.find("S"),
        end=grid.find("E"),
        passable_values=set(".SE")
    ))

    for path in paths:
        pretty(grid, highlight_path=path)
        direction = 1
        score = 0
        for p1, p2 in itertools.pairwise(path):
            new_direction = get_direction(p1, p2)
            if new_direction != direction:
                score += 1000
            score += 1
            direction = new_direction


def pretty(grid: LineGrid, highlight_path: list[tuple[int, int]] = None):
    if highlight_path is None:
        highlight_path = []

    from PIL import Image
    image = Image.new(size=(grid.width, grid.height), mode="RGB")

    colours = [
        colour.hsl2rgb(c) for c in colour.color_scale(
            colour.rgb2hsl((1, 0, 0)),
            colour.rgb2hsl((0, 0, 1)),
            len(highlight_path)
        )
    ]
    for y in range(grid.height):
        for x in range(grid.width):
            v = grid.get(x, y)
            if v == "S":
                image.putpixel((x, y), (0, 255, 0))
            elif v == "E":
                image.putpixel((x, y), (255, 0, 0))
            elif (x, y) in highlight_path:
                col = tuple([int(c * 255) for c in colours[highlight_path.index((x, y))]])
                image.putpixel((x, y), col)
            elif v == "#":
                image.putpixel((x, y), (0, 0, 0))
                present_neighbours = []
                for nx, ny in [grid.get_neighbour_coord(x, y, d) for d in [0, 2, 4, 6]]:
                    if grid.is_pos_in_bounds(nx, ny):
                        present_neighbours.append(grid.get(nx, ny) == "#")
                    else:
                        present_neighbours.append(False)
            else:
                image.putpixel((x, y), (255, 255, 255))

    image.save("pretty_input.png")


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
