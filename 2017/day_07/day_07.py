import dataclasses
import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2017/day/7
"""

_INPUT_PATH = INPUT_PATH_TEST


@dataclasses.dataclass
class Process:
    name: str
    weight: int
    children_names: list[str]
    children: list['Process']
    parent: Optional['Process'] = None

    @property
    def total_weight(self) -> int:
        return self.weight + sum([c.total_weight for c in self.children])


def load() -> dict[str, Process]:
    processes: dict[str, Process] = {}
    for line in input_lines(_INPUT_PATH):
        if "->" in line:
            m = re.match(r"([a-z]*) \((\d*)\) -> ([a-z, ]*)", line)
            parts = m.groups()
            processes[parts[0]] = Process(
                name=parts[0],
                weight=int(parts[1]),
                children_names=parts[2].split(", "),
                children=[]
            )
        else:
            m = re.match(r"([a-z]*) \((\d*)\)", line)
            parts = m.groups()
            processes[parts[0]] = Process(parts[0], int(parts[1]), [], [])

    for process in processes.values():
        for child_name in process.children_names:
            processes[child_name].parent = process
            process.children.append(processes[child_name])

    return processes


def find_root(processes: dict[str, Process]) -> Process:
    p: Process = list(processes.values())[0]
    while True:
        if p.parent is None:
            return p
        else:
            p = p.parent


def part_1() -> Union[int, str]:
    processes = load()
    return find_root(processes).name


def part_2() -> Union[int, str]:
    processes = load()
    process = find_root(processes)

    done = False
    while not done:
        min_weight



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
