import itertools
import re
from functools import cache
from pathlib import Path
from typing import Union, Iterator, Optional, Type, Any, Iterable
from math import inf


"""
https://adventofcode.com/2022/day/16
"""


def raw_input(input_path: Path = Path("input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read()
    return data


def input_lines(input_path: Path = Path("input.txt"), convert_type: Optional[Type] = None) -> Iterator[Any]:
    for line in raw_input(input_path).strip().split("\n"):
        if convert_type is None:
            yield line.strip()
        else:
            yield convert_type(line.strip())


@cache
def calc_total_release(
        start_node: str,
        node_distances: dict[str, dict[str, int]],
        node_rates: dict[str, int],
        order: Iterable[str],
        time: int) -> int:
    total = 0
    time_remaining = time
    current_pos = start_node
    for valve in order:
        time_remaining -= node_distances[current_pos][valve]
        time_remaining -= 1  # -1 for valve opening time
        total += time_remaining * node_rates[valve]
        current_pos = valve
        if time_remaining <= 0:
            break

    return total


def part_1() -> Union[int, str]:
    node_distances = {}
    node_connections = {}
    node_rates = {}

    for line in input_lines(input_path=Path("test_input.txt")):
        name = re.search(r"(\w{2})(?= has)", line).group()
        connections = re.findall(r"(\w{2})(?=,|$)", line)
        rate = int(re.search(r"(\d+)(?=;)", line).group())
        node_connections[name] = connections
        node_rates[name] = rate

    # Calculate distances
    for root, connections in node_connections.items():
        unvisited = list(node_connections.keys())
        distances = {u: 0 if u == root else inf for u in unvisited}

        current = root
        while True:
            for neighbour in node_connections[current]:
                if neighbour in unvisited:
                    tentative = distances[current] + 1
                    distances[neighbour] = min(tentative, distances[neighbour])

            unvisited.remove(current)
            if len(unvisited):
                min_distance = inf
                min_key = ""
                for u in unvisited:
                    if distances[u] < min_distance:
                        min_key = u
                        min_distance = distances[u]
                if min_distance == inf:
                    break
                current = min_key
            else:
                break
        node_distances[root] = dict(distances)

    viable_nodes = [n for n in node_rates if node_rates[n]]

    order: tuple[str, ...]
    final_order = []
    remaining = list(viable_nodes)

    while remaining:
        best_value = 0
        best_next_node = ""
        for check in remaining:
            maybe = calc_total_release(
                start_node="AA",
                node_distances=node_distances,
                node_rates=node_rates,
                order=final_order + [check],
                time=30
            )
            if maybe > best_value:
                best_value = maybe
                best_next_node = check
        print(f"best next: {repr(best_next_node)}")
        remaining.remove(best_next_node)
        final_order.append(best_next_node)

    print(final_order)

    return calc_total_release(
                start_node="AA",
                node_distances=node_distances,
                node_rates=node_rates,
                order=final_order,
                time=30
            )


def part_2() -> Union[int, str]:
    ...


if __name__ == "__main__":
    print("Part 1:", part_1())
    print()
    print("Part 2:", part_2())
