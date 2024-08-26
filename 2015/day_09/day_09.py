import re
import time
from itertools import permutations, combinations, pairwise

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/9
"""


def part_1() -> Union[int, str]:
    city_names: list[str] = []
    distances: dict[str, int] = {}

    for line in input_lines(INPUT_PATH):
        city_1, city_2, dist_str = re.match(r"(\w+) to (\w+) = (\d+)", line).groups()
        city_names.append(city_1)
        city_names.append(city_2)
        key: str = "-".join(sorted((city_1, city_2)))
        distances[key] = int(dist_str)
    city_names = list(set(city_names))

    shortest = inf
    for permutation in permutations(city_names, len(city_names)):
        route_distance = 0
        for a, b in pairwise(permutation):
            key: str = "-".join(sorted((a, b)))
            route_distance += distances[key]
        if route_distance < shortest:
            shortest = route_distance
    return shortest


def part_2() -> Union[int, str]:
    city_names: list[str] = []
    distances: dict[str, int] = {}

    for line in input_lines(INPUT_PATH):
        city_1, city_2, dist_str = re.match(r"(\w+) to (\w+) = (\d+)", line).groups()
        city_names.append(city_1)
        city_names.append(city_2)
        key: str = "-".join(sorted((city_1, city_2)))
        distances[key] = int(dist_str)
    city_names = list(set(city_names))

    longest = 0
    for permutation in permutations(city_names, len(city_names)):
        route_distance = 0
        for a, b in pairwise(permutation):
            key: str = "-".join(sorted((a, b)))
            route_distance += distances[key]
        if route_distance > longest:
            longest = route_distance
    return longest


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
