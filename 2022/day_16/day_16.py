import re
from itertools import combinations
from math import inf
from typing import List, Dict, Union, Set, FrozenSet


def get_routes(connections: Dict[str, List[str]]):
    routes: Dict[FrozenSet[str], int] = {}

    target_num_routes = len(list(combinations(list(connections.keys()), 2)))

    for c in connections:
        for d in connections[c]:
            routes[frozenset({c, d})] = 1

    for start in connections:
        for end in connections:
            if (frozenset({start, end}) in routes) or (start == end):
                continue

            unvisited_nodes = list(connections.keys())
            distances: Dict[str, Union[int, float]] = {}
            reached_from: Dict[str, str] = {}
            for c in unvisited_nodes:
                distances[c] = inf
            distances[start] = 0

            while True:
                subject_node = list(sorted(unvisited_nodes, key=lambda x: distances[x]))[0]
                unvisited_nodes.remove(subject_node)
                if subject_node == end:
                    break
                for test_node in connections[subject_node]:
                    if distances[subject_node] + 1 < distances[test_node]:
                        distances[test_node] = distances[subject_node] + 1
                        reached_from[test_node] = subject_node

            route = [end]
            while True:
                next_node = reached_from[route[0]]
                route.insert(0, next_node)
                if next_node == start:
                    break

            for i in range(len(route)):
                for j in range(i + 1, len(route)):
                    routes[frozenset({route[i], route[j]})] = distances[route[j]] - distances[route[i]]

    assert len(routes) == target_num_routes

    return routes


def main():
    flow_rates: Dict[str, int] = {}
    raw_connections: Dict[str, List[str]] = {}

    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            res = re.findall(r".* ([A-Z]{2}) .*=(\d*); .* valves? ([A-Z]{2}(, [A-Z]{2})*)", line.strip())[0]
            flow_rates[res[0]] = int(res[1])
            raw_connections[res[0]] = res[2].split(", ")

    routes = get_routes(raw_connections)

      



if __name__ == '__main__':
    main()
    """
    print(
        get_total_pressure_release(
            [
                Node.nodes["DD"],
                "on",
                Node.nodes["CC"],
                Node.nodes["BB"],
                "on",
                Node.nodes["AA"],
                Node.nodes["II"],
                Node.nodes["JJ"],
                "on",
                Node.nodes["II"],
                Node.nodes["AA"],
                Node.nodes["DD"],
                Node.nodes["EE"],
                Node.nodes["FF"],
                Node.nodes["GG"],
                Node.nodes["HH"],
                "on",
                Node.nodes["GG"],
                Node.nodes["FF"],
                Node.nodes["EE"],
                "on",
                Node.nodes["DD"],
                Node.nodes["CC"],
                "on",
                "wait",
                "wait",
                "wait",
                "wait",
                "wait",
                "wait",
            ]
        )
    )
    """
