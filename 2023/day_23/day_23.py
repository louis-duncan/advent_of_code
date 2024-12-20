import time
import sys
from functools import cache

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2023/day/23
"""

def get_map(part="part_1") -> [dict[NodeWithDistance], NodeWithDistance, NodeWithDistance]:
    line_grid = LineGrid(input_lines("input.txt"))
    nodes: dict[tuple[int, int], NodeWithDistance] = {}
    start_x = line_grid.get_row(0).index(".")
    end_x = line_grid.get_row(-1).index(".")
    for x, y, in line_grid.iterate_x_y():
        if line_grid.get(x, y) != "#":
            nodes[(x, y)] = NodeWithDistance()

    start = nodes[(start_x, 0)]
    end = nodes[(end_x, line_grid.height - 1)]

    for x, y in nodes:
        here = line_grid.get(x, y)
        if here == "." or part == "part_2":
            for direction in range(4):
                n_coord = line_grid.get_neighbour_coord(x, y, direction)
                try:
                    n = line_grid.get(*n_coord)
                    if n != "#":
                        nodes[(x, y)].connections[nodes[n_coord]] = 1
                except ValueError:
                    pass
        else:
            allowed_direction = "^>v<".find(here)
            try:
                n_coord = line_grid.get_neighbour_coord(x, y, allowed_direction)
                nodes[(x, y)].connections[nodes[n_coord]] = 1
            except ValueError:
                pass

    return nodes, start, end


def get_path_end(start_node: NodeWithDistance, next_node: NodeWithDistance) -> [NodeWithDistance, int]:
    prev = start_node
    current = next_node
    distance = start_node.connections[next_node]
    while len(current.connections) == 2:
        pos_connections: dict[NodeWithDistance, int] = current.connections.copy()
        pos_connections.pop(prev)

        assert len(pos_connections) == 1
        prev = current
        current, d = list(pos_connections.items())[0]

        distance += d

    return current, distance


def simplify_map(nodes: dict[tuple[int, int], NodeWithDistance]):
    for _, node in nodes.items():
        if len(node.connections) != 2:
            new_connections: dict[NodeWithDistance, int] = {}
            for connection_node, connection_dist in node.connections.items():
                new_node, new_distance = get_path_end(node, connection_node)
                new_connections[new_node] = new_distance
            node.connections = new_connections


def longest_path(node: NodeWithDistance, end: None, visited: Optional[tuple[NodeWithDistance]] = None) -> [list[NodeWithDistance], int]:
    if visited is None:
        new_visited = (node, )
    else:
        new_visited = visited + (node,)

    route_nodes: list[NodeWithDistance] = []
    route_len: int = 0
    for connection, dist in node.connections.items():
        if connection not in new_visited:
            new_route_nodes, new_route_len = longest_path(connection, end, new_visited)
            new_route_len += dist
            if (new_route_len > route_len) and (new_route_nodes[-1] is end):
                route_nodes = new_route_nodes
                route_len = new_route_len

    route_nodes.insert(0, node)
    return route_nodes, route_len


def part_1() -> Union[int, str]:
    sys.setrecursionlimit(10000)
    nodes, start, end = get_map("part_1")
    simplify_map(nodes)
    path, length = longest_path(start, end)
    return length


def part_2() -> Union[int, str]:
    sys.setrecursionlimit(10000)
    nodes, start, end = get_map("part_2")
    simplify_map(nodes)
    path, length = longest_path(start, end)
    return length


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
