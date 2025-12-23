import dataclasses
import re
import time
from functools import cached_property
from typing import Union, Optional, Callable

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/11
"""

_INPUT_PATH = au.INPUT_PATH_TEST


@dataclasses.dataclass
class Node:
    label: str
    connections: list['Node'] = dataclasses.field(default_factory=list)

    def __eq__(self, other) -> bool:
        if isinstance(other, Node):
            return self.label == other.label
        elif isinstance(other, str):
            return self.label == other
        else:
            return False

    @cached_property
    def reachable(self) -> set['Node']:
        r = set()
        for n in self.connections:
            r.add(n)
            r = r.union(n.reachable)
        return r

    def __hash__(self) -> int:
        return hash(self.label)

    def __repr__(self) -> str:
        return f"Node(label={self.label}, connections=*{len(self.connections)})"


def traverse(
        route: tuple[Node, ...],
        target: Union[Node, str],
        cache: dict[tuple[Node, Node], int],
        valid_check: Optional[Callable] = None
) -> int:
    if (route[-1], target) in cache:
        return cache[(route[-1], target)]

    total = 0
    for c in route[-1].connections:
        if c.label == target:
            total += 1
        elif c not in route:
            if target in c.reachable:
                total += traverse(route + (c, ), target, cache)
            else:
                pass

    if valid_check is None or valid_check(route):
        cache[(route[-1], target)] = total

    return total


def part_1() -> Union[int, str]:
    lines = list(au.input_lines(test=False))
    all_nodes: dict[str, Node] = {"out": Node("out")}
    for line in lines:
        l = line.split(":")[0]
        all_nodes[l] = Node(l)
    for line in lines:
        l, *cs = re.findall(r"\w+", line)
        for c in cs:
            all_nodes[l].connections.append(all_nodes[c])

    count_cache: dict[tuple[Node, Node], int] = {}
    return traverse(
        (all_nodes["you"],),
        "out",
        count_cache
    )


def part_2() -> Union[int, str]:
    lines = list(au.input_lines(test=False))
    all_nodes: dict[str, Node] = {"out": Node("out")}
    for line in lines:
        l = line.split(":")[0]
        all_nodes[l] = Node(l)
    for line in lines:
        l, *cs = re.findall(r"\w+", line)
        for c in cs:
            all_nodes[l].connections.append(all_nodes[c])

    start = all_nodes["svr"]
    dac = all_nodes["dac"]
    fft = all_nodes["fft"]
    out = all_nodes["out"]

    # Pre-load caches
    for n in all_nodes.values():
        _ = n.reachable

    sd = traverse(
        (start,),
        dac,
        {},
        valid_check=lambda r: fft not in r
    )
    sf = traverse(
        (start,),
        fft,
        {},
        valid_check=lambda r: dac not in r
    )
    df = traverse(
        (dac,),
        fft,
        {}
    )
    fd = traverse(
        (fft,),
        dac,
        {}
    )
    do = traverse(
        (dac,),
        out,
        {}
    )
    fo = traverse(
        (fft,),
        out,
        {}
    )

    a = sd * df * fo
    b = sf * fd * do
    return a + b


if __name__ == "__main__":
    p1_start = time.time()
    part_1_answer = part_1()
    p1_duration = time.time() - p1_start
    assert part_1_answer == 506
    if part_1_answer is not None:
        print(f"Part 1 ({p1_duration * 1000:.2f}ms):", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    p2_start = time.time()
    part_2_answer = part_2()
    p2_duration = time.time() - p2_start
    assert part_2_answer == 385912350172800
    if part_2_answer is not None:
        print(f"Part 2 ({p2_duration * 1000:.2f}ms):", part_2_answer)
        pyperclip.copy(part_2_answer)
