import dataclasses
import re
import time
from math import inf
from typing import Union, Optional

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/8
"""

_INPUT_PATH = au.INPUT_PATH_TEST


@dataclasses.dataclass
class Circuit:
    nodes: set['Node'] = dataclasses.field(default_factory=set)

    def add(self, new: 'Node'):
        self.nodes.add(new)

    def __add__(self, other: 'Circuit') -> 'Circuit':
        new = Circuit()
        new.nodes = self.nodes.union(other.nodes)
        return new


class Node(au.Point3):
    def __init__(self, x: au.t_num, y: au.t_num, z: au.t_num, cloud=None):
        super().__init__(x, y, z, cloud)
        self.connections: list['Node'] = []
        self.circuit: Circuit = Circuit()
        self.circuit.add(self)


    def add_connection(self, other: 'Node', distances=None):
        self.connections.append(other)
        other.connections.append(self)
        self.circuit.add(other)
        other.circuit.add(self)

        new_circuit = self.circuit + other.circuit

        """
        if distances:
            for n in self.circuit.nodes:
                if hash(other) < hash(n):
                    t = (other, n)
                else:
                    t = (n, other)
                try:
                    distances.pop(t)
                except KeyError:
                    pass
            for n in other.circuit.nodes:
                if hash(self) < hash(n):
                    t = (self, n)
                else:
                    t = (n, self)
                try:
                    distances.pop(t)
                except KeyError:
                    pass
        """

        for n in new_circuit.nodes:
            n.circuit = new_circuit


def part_1() -> Union[int, str]:
    test = False

    cloud = au.Point3Cloud()
    for line in au.input_lines(test=test):
        parts = re.findall(r"\d+", line)
        Node(
            int(parts[0]),
            int(parts[1]),
            int(parts[2]),
            cloud=cloud
        )

    distances: dict[tuple[Node, Node], float] = {}

    # noinspection PyTypeChecker
    list_points: list[Node] = list(cloud.points)

    for i in range(len(list_points)):
        for j in range(i + 1, len(cloud.points)):
            p1 = list_points[i]
            p2 = list_points[j]

            if hash(p1) < hash(p2):
                t = (p1, p2)
            else:
                t = (p2, p1)

            distances[t] = p1 / p2

    print("Distances calculated...")

    sorted_pairings = sorted(list(distances.keys()), key=distances.get, reverse=False)

    for i in range(10 if test else 1000):
        min_pair = sorted_pairings[i]
        if min_pair[0].circuit is not min_pair[1].circuit:
            min_pair[0].add_connection(min_pair[1])

    print("Connections calculated...")

    circuits = set()
    for p in list_points:
        if len(p.circuit.nodes) > 1:
            circuits.add(len(p.circuit.nodes))
    circuits = sorted(list(circuits), reverse=True)
    while len(circuits) < 3:
        circuits.append(1)

    return circuits[0] * circuits[1] * circuits[2]



def part_2() -> Union[int, str]:
    test = False

    cloud = au.Point3Cloud()
    for line in au.input_lines(test=test):
        parts = re.findall(r"\d+", line)
        Node(
            int(parts[0]),
            int(parts[1]),
            int(parts[2]),
            cloud=cloud
        )

    distances: dict[tuple[Node, Node], float] = {}

    # noinspection PyTypeChecker
    list_points: list[Node] = list(cloud.points)

    for i in range(len(list_points)):
        for j in range(i + 1, len(cloud.points)):
            p1 = list_points[i]
            p2 = list_points[j]

            if hash(p1) < hash(p2):
                t = (p1, p2)
            else:
                t = (p2, p1)

            distances[t] = p1 / p2

    print("Distances calculated...")

    sorted_pairings = sorted(list(distances.keys()), key=distances.get, reverse=False)

    last_pair = None
    for pairing in sorted_pairings:
        if pairing[0].circuit is not pairing[1].circuit:
            pairing[0].add_connection(pairing[1])
            last_pair = pairing

    print("Connections calculated...")
    assert last_pair is not None

    return last_pair[0].x * last_pair[1].x


if __name__ == "__main__":
    p1_start = time.time()
    part_1_answer = part_1()
    p1_duration = time.time() - p1_start
    assert part_1_answer == 75680
    if part_1_answer is not None:
        print(f"Part 1 ({p1_duration * 1000:.2f}ms):", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    p2_start = time.time()
    part_2_answer = part_2()
    p2_duration = time.time() - p2_start
    assert part_2_answer == 8995844880
    if part_2_answer is not None:
        print(f"Part 2 ({p2_duration * 1000:.2f}ms):", part_2_answer)
        pyperclip.copy(part_2_answer)
