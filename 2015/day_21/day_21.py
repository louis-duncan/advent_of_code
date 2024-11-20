import dataclasses
import itertools
import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/21
"""

_INPUT_PATH = INPUT_PATH  # _TEST


@dataclasses.dataclass
class Character:
    name: str
    hp: int
    damage: int
    armour: int


@dataclasses.dataclass
class Item:
    name: str
    cost: int
    damage: int
    armour: int

WEAPONS = (
    Item("Dagger", 8, 4, 0),
    Item("Shortsword", 10, 5, 0),
    Item("Warhammer", 25, 6, 0),
    Item("Longsword", 40, 7, 0),
    Item("Greataxe", 74, 8, 0),
)

ARMOUR = (
    Item("Leather", 13, 0, 1),
    Item("Chainmail", 31, 0, 2),
    Item("Splintmail", 53, 0, 3),
    Item("Bandedmail", 75, 0, 4),
    Item("Platemail", 102, 0, 5),
    Item("None", 0, 0, 0),
)

RINGS = (
    Item("Damage +1", 25, 1, 0),
    Item("Damage + 2", 50, 2, 0),
    Item("Damage + 3", 100, 3, 0),
    Item("Defense + 1", 20, 0, 1),
    Item("Defense + 2", 40, 0, 2),
    Item("Defense + 3", 80, 0, 3),
    Item("No ring 1", 0, 0, 0),
    Item("No ring 2", 0, 0, 0),
)


def resolve(player_1: Character, player_2: Character) -> Character:
    attacker = player_1
    defender = player_2
    while player_1.hp > 0 and player_2.hp > 0:
        defender.hp -= max(1, attacker.damage - defender.armour)
        attacker, defender = defender, attacker

    return player_1 if player_2.hp <= 0 else player_2


def item_combinations():
    ring_1: Item
    ring_2: Item
    for weapon in WEAPONS:
        for armour in ARMOUR:
            for ring_1, ring_2 in itertools.combinations(RINGS, r=2):
                yield weapon, armour, ring_1, ring_2


def part_1() -> Union[int, str]:
    boss = Character("boss", *[int(n) for n in re.findall(r"\d+", raw_input(_INPUT_PATH), flags=re.MULTILINE)])
    boss_stats = [int(n) for n in re.findall(r"\d+", raw_input(_INPUT_PATH), flags=re.MULTILINE)]
    player = Character("player", 100, 0, 0)

    best_comb: list[Item] = []
    best_cost = 10000
    for weapon, armour, ring_1, ring_2 in item_combinations():
        player.hp = 100
        player.damage = weapon.damage + ring_1.damage + ring_2.damage
        player.armour = armour.armour + ring_1.armour + ring_2.armour
        boss.hp = boss_stats[0]
        winner = resolve(player, boss)
        if winner is player:
            cost = weapon.cost + armour.cost + ring_1.cost + ring_2.cost
            if cost < best_cost:
                best_comb = [weapon, armour, ring_1, ring_2]
                best_cost = cost

    print(best_cost, best_comb)
    return best_cost


def part_2() -> Union[int, str]:
    boss = Character("boss", *[int(n) for n in re.findall(r"\d+", raw_input(_INPUT_PATH), flags=re.MULTILINE)])
    boss_stats = [int(n) for n in re.findall(r"\d+", raw_input(_INPUT_PATH), flags=re.MULTILINE)]
    player = Character("player", 100, 0, 0)

    worst_comb: list[Item] = []
    worst_cost = 0
    for weapon, armour, ring_1, ring_2 in item_combinations():
        player.hp = 100
        player.damage = weapon.damage + ring_1.damage + ring_2.damage
        player.armour = armour.armour + ring_1.armour + ring_2.armour
        boss.hp = boss_stats[0]
        winner = resolve(player, boss)
        if winner is boss:
            cost = weapon.cost + armour.cost + ring_1.cost + ring_2.cost
            if cost > worst_cost:
                worst_comb = [weapon, armour, ring_1, ring_2]
                worst_cost = cost

    print(worst_cost, worst_comb)
    return worst_cost


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
