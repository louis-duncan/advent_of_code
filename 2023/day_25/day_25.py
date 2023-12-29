import time
import re
from itertools import pairwise

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2023/day/25
"""


def get_from_value(d: dict[Any, Any], value: Any):
    for k, v in d.items():
        if v == value:
            return k


def get_smallest(values: dict[Node, Union[int, float]], mask: set[Node]) -> Node:
    assert len(mask) > 0
    for key, value in sorted(list(values.items()), key=lambda x: x[1]):
        if key in mask: return key
    raise ValueError("No smallest in mask")


def find_distances(start: Node, all_nodes: list[Node]) -> [dict[Node, Union[int, float]], dict[Node, Optional[Node]]]:
    unvisited_nodes = all_nodes.copy()
    distances: dict[Node, Union[int, float]] = {}
    previous: dict[Node, Optional[Node]] = {}
    queue: set[Node] = set()

    for node in unvisited_nodes:
        distances[node] = inf
        previous[node] = None
        queue.add(node)

    distances[start] = 0

    while len(queue) > 0:
        current = get_smallest(distances, queue)
        queue.remove(current)

        for neighbour in current.connections:
            if neighbour in queue:
                alt = distances[current] + 1
                if alt < distances[neighbour]:
                    distances[neighbour] = alt
                    previous[neighbour] = current

    return distances, previous


def get_sub_routes(route: list[Node]) -> list[list[Node]]:
    sub_routes: list[list[Node]] = []
    for i in range(len(route)):
        for j in range(i + 1, len(route)):
            sub_routes.append(route[i:j + 1])
    return sub_routes


def get_route(
        end: Node,
        previous: dict[Node, Optional[Node]]
) -> list[Node]:
    route: list[Node] = [end]
    done = False
    while not done:
        new = previous[route[-1]]
        if new is None:
            done = True
        else:
            route.append(new)
    return route[::-1]


def get_transitions(route: list[Node]) -> list[tuple[Node, Node]]:
    transitions: list[tuple[Node, Node]] = []
    for a, b in pairwise(route):
        if hash(a) < hash(b):
            transitions.append((a, b))
        else:
            transitions.append((b, a))
    return transitions


def get_routes(
        distances: dict[Node, Union[int, float]],
        previous: dict[Node, Optional[Node]]
) -> dict[tuple[Node, Node], list[Node]]:
    routes: dict[tuple[Node, Node], list[Node]] = {}

    for end_node in distances:
        new_route = get_route(end_node, previous)
        all_sub_routes = get_sub_routes(new_route)
        for sub_route in all_sub_routes:
            if hash(sub_route[0]) < hash(sub_route[-1]):
                key = (sub_route[0], sub_route[-1])
            else:
                key = (sub_route[-1], sub_route[0])
            assert len(key) == 2
            routes[key] = sub_route

    return routes


def part_1() -> Union[int, str]:
    nodes: dict[str, Node] = {}
    for line in input_lines("input.txt"):
        names = re.findall(r"\w+", line)

        if names[0] not in nodes:
            new = Node()
            new.value = names[0]
            nodes[names[0]] = new

        for n in names[1:]:
            if n not in nodes:
                new = Node()
                new.value = n
                nodes[n] = new
            nodes[names[0]].connections.add(nodes[n])
            nodes[n].connections.add(nodes[names[0]])

    routes: dict[tuple[Node, Node], list[Node]] = {}
    nodes_list = list(nodes.values())
    counts: dict[tuple[Node, Node], int] = {}

    for i in range(len(nodes_list)):
        for j in range(i + 1, len(nodes_list)):
            if (nodes_list[i], nodes_list[j]) in routes:
                continue

            start = nodes_list[i]

            distances, previous = find_distances(start, nodes_list)
            new_routes = get_routes(distances, previous)
            for route in new_routes.values():
                transitions = get_transitions(route)
                for transition in transitions:
                    if transition not in counts:
                        counts[transition] = 1
                    else:
                        counts[transition] += 1

    for transition, count in sorted(list(counts.items()), key=lambda x: x[1], reverse=True):
        print(transition[0].value, transition[1].value, count)


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
