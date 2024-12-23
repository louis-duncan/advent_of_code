import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/23
"""

_INPUT_PATH = INPUT_PATH_TEST


class Node:
    def __init__(self, name: str):
        self.name = name
        self.connections: list[Node] = []


def part_1() -> Union[int, str]:
    connections: dict[str, set[str]] = {}

    for line in input_lines(_INPUT_PATH):
        node_1, node_2 = re.findall(r"[a-z]+", line)
        if node_1 not in connections:
            connections[node_1] = set()
        connections[node_1].add(node_2)
        if node_2 not in connections:
            connections[node_2] = set()
        connections[node_2].add(node_1)

    groups: list[set[str]] = []
    while connections:
        to_pop = [list(connections.keys())[0]]
        group: set[str] = set()
        while to_pop:
            current = to_pop.pop(0)
            if current in group:
                continue
            group.add(current)
            for n in connections[current]:
                if n not in to_pop:
                    to_pop.append(n)
            connections.pop(current)
        groups.append(group)

    pass




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
