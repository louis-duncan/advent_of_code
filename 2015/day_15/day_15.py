import itertools
import re
import time
from dataclasses import dataclass
from functools import cache
from statistics import quantiles

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/15
"""

_INPUT_PATH = INPUT_PATH  # _TEST


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavour: int
    texture: int
    calories: int



def part_1() -> Union[int, str]:
    ingredients: list[Ingredient] = []

    @cache
    def get_score(_quantities: tuple[int, ...]) -> int:
        capacity = 0
        durability = 0
        flavour = 0
        texture = 0
        for i, ingredient in enumerate(ingredients):
            capacity += ingredient.capacity * _quantities[i]
            durability += ingredient.durability * _quantities[i]
            flavour += ingredient.flavour * _quantities[i]
            texture += ingredient.texture * _quantities[i]

        return max(0, capacity) * max(0, durability) * max(0, flavour) * max(0, texture)

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

    names = [i.name for i in ingredients]
    best = 0
    for comb in itertools.combinations_with_replacement(names, r=100):
        quantities = tuple((comb.count(n) for n in names))
        if (score := get_score(quantities)) > best:
            best = score

    return best


def part_2() -> Union[int, str]:
    ingredients: list[Ingredient] = []

    @cache
    def get_score(_quantities: tuple[int, ...]) -> int:
        capacity = 0
        durability = 0
        flavour = 0
        texture = 0
        calories = 0
        for i, ingredient in enumerate(ingredients):
            capacity += ingredient.capacity * _quantities[i]
            durability += ingredient.durability * _quantities[i]
            flavour += ingredient.flavour * _quantities[i]
            texture += ingredient.texture * _quantities[i]
            calories += ingredient.calories * _quantities[i]

        if calories == 500:
            return max(0, capacity) * max(0, durability) * max(0, flavour) * max(0, texture)
        else:
            return 0

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

    names = [i.name for i in ingredients]
    best = 0
    for comb in itertools.combinations_with_replacement(names, r=100):
        quantities = tuple((comb.count(n) for n in names))
        if (score := get_score(quantities)) > best:
            best = score

    return best


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
