import time
import re

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2023/day/25
"""


def part_1() -> Union[int, str]:
    nodes: dict[str, Node] = {}
    for line in input_lines("test_input.txt"):
        names = re.findall(r"\w+", line)

        if names[0] not in nodes:
            nodes[names[0]] = Node()

        for n in names[1:]:
            if n not in nodes:
                nodes[n] = Node()
            nodes[names[0]].connections.add(nodes[n])
            nodes[n].connections.add(nodes[names[0]])

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
