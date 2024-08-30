import re
import time
from dataclasses import dataclass

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/15
"""

_INPUT_PATH = INPUT_PATH_TEST


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavour: int
    texture: int
    calories: int


def get_score_1(ingredients: list[Ingredient], quantities: dict[str, int]) -> int:
    score = 0
    for ingredient in ingredients:




def part_1() -> Union[int, str]:
    ingredients: list[Ingredient] = []
    quantities: dict[str, int] = {}
    for line in input_lines(_INPUT_PATH):
        name, capacity_str, durability_str, flavour_str, texture_str, calories_str = re.match(
            r"(\w+): \w+ (.+?), \w+ (.+?), \w+ (.+?), \w+ (.+?), \w+ (.+?)", line
        ).groups()
        ingredients.append(
            Ingredient(
                name=name,
                capacity=int(capacity_str),
                durability=int(durability_str),
                flavour=int(flavour_str),
                texture=int(texture_str),
                calories=int(calories_str)
            )
        )
        quantities[name] = 0




def part_2() -> Union[int, str]:
    ...


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
