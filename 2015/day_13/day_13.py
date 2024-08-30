import json
import re
import time
from itertools import permutations, pairwise, chain

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/13
"""

_INPUT_PATH = INPUT_PATH


def part_1() -> Union[int, str]:
    lines = input_lines(_INPUT_PATH)
    names: list[str] = []
    weights: dict[str, int] = {}
    for line in lines:
        name_1, effect, weight, name_2 = re.match(r"(\w+) would (\w+) (\d+).* (\w+)", line).groups()
        if name_1 not in names:
            names.append(name_1)

        key = "-".join(sorted((name_1, name_2)))

        if key not in weights:
            weights[key] = 0

        weights[key] += int(weight) if effect == "gain" else -int(weight)

    best_happiness = -inf
    for permutation in permutations(names, r=len(names)):
        total_happiness = 0
        for name_1, name_2 in pairwise(chain(permutation, [permutation[0]])):
            key = "-".join(sorted((name_1, name_2)))
            total_happiness += weights[key]

        if total_happiness > best_happiness:
            best_happiness = total_happiness

    return best_happiness


def part_2() -> Union[int, str]:
    lines = input_lines(_INPUT_PATH)
    names: list[str] = ["Me"]
    weights: dict[str, int] = {}
    for line in lines:
        name_1, effect, weight, name_2 = re.match(r"(\w+) would (\w+) (\d+).* (\w+)", line).groups()
        if name_1 not in names:
            names.append(name_1)

        key = "-".join(sorted((name_1, name_2)))

        if key not in weights:
            weights[key] = 0

        weights[key] += int(weight) if effect == "gain" else -int(weight)

    best_happiness = -inf
    for permutation in permutations(names, r=len(names)):
        total_happiness = 0
        for name_1, name_2 in pairwise(chain(permutation, [permutation[0]])):
            key = "-".join(sorted((name_1, name_2)))
            total_happiness += weights.get(key, 0)

        if total_happiness > best_happiness:
            best_happiness = total_happiness

    return best_happiness


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
