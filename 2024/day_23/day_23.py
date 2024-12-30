import itertools
import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/23
"""

_INPUT_PATH = INPUT_PATH  # _TEST


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

    three_node_groups: set[tuple[str, str, str]] = set()

    for node in connections:
        for a, b in itertools.combinations(connections[node], 2):
            if a in connections[b]:
                # noinspection PyTypeChecker
                trio: tuple[str, str, str] = tuple(sorted((node, a, b)))
                three_node_groups.add(trio)

    result = 0
    for t in three_node_groups:
        for n in t:
            if n.startswith("t"):
                result += 1
                break
    return result



def part_2() -> Union[int, str]:
    connections: dict[str, set[str]] = {}

    for line in input_lines(_INPUT_PATH):
        node_1, node_2 = re.findall(r"[a-z]+", line)
        if node_1 not in connections:
            connections[node_1] = set()
        connections[node_1].add(node_2)
        if node_2 not in connections:
            connections[node_2] = set()
        connections[node_2].add(node_1)

    groups: set[tuple[str, ...]] = set()

    to_check = list(connections.keys())
    for root in to_check:
        possible_group = [root] + list(connections[root])
        for i in range(len(possible_group) - 1, 0, -1):
            for j in range(1, i, 1):
                if possible_group[i] not in connections[possible_group[j]]:
                    possible_group.remove(possible_group[i])
                    break
        groups.add(tuple(sorted(possible_group)))

    biggest = set()
    for group in groups:
        if len(group) > len(biggest):
            biggest = group
    return ",".join(biggest)


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
