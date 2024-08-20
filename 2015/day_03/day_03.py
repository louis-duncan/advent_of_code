import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/3
"""


def part_1() -> Union[int, str]:
    moves = raw_input(INPUT_PATH)
    x, y = 0, 0
    totals = {(x, y): 1}
    for move in moves:
        if move == ">":
            x += 1
        elif move == "<":
            x -= 1
        elif move == "^":
            y += 1
        elif move == "v":
            y -= 1
        if (x, y) in totals:
            totals[(x, y)] += 1
        else:
            totals[(x, y)] = 0
    return len(totals)


def part_2() -> Union[int, str]:
    moves = raw_input(INPUT_PATH)
    santa = Point("",0, 0)
    robo = Point("", 0, 0)
    santa_totals = {(0, 0): 1}
    robo_totals = {(0, 0): 1}
    for i, move in enumerate(moves):
        if i % 2 == 0:
            agent = santa
            totals = santa_totals
        else:
            agent = robo
            totals = robo_totals
        if move == ">":
            agent.x += 1
        elif move == "<":
            agent.x -= 1
        elif move == "^":
            agent.y += 1
        elif move == "v":
            agent.y -= 1
        if (agent.x, agent.y) in totals:
            totals[(agent.x, agent.y)] += 1
        else:
            totals[(agent.x, agent.y)] = 0
    santa_houses = set(santa_totals.keys())
    robo_houses = set(robo_totals.keys())
    return len(santa_houses.union(robo_houses))


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
