import dataclasses
import itertools
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/17
"""

_INPUT_PATH = INPUT_PATH  #_TEST


@dataclasses.dataclass
class Container:
    id: int
    volume: int

    def __hash__(self):
        return hash(self.id)

    def __add__(self, other) -> int:
        if isinstance(other, int):
            return self.volume + other
        elif isinstance(other, Container):
            return self.volume + other.volume


def part_1() -> Union[int, str]:
    containers = [Container(i, int(v.strip())) for i, v in enumerate(input_lines(_INPUT_PATH))]
    containers.sort(key=lambda x: x.volume)
    target = 150

    tot = 0
    for min_num_containers in range(1, len(containers)):
        tot += containers[-min_num_containers].volume
        if tot >= target:
            break
    else:
        min_num_containers = 1

    tot = 0
    for max_num_containers in range(len(containers)):
        tot += containers[max_num_containers].volume
        if tot >= target:
            break
    else:
        max_num_containers = len(containers)

    options = set()
    for n in range(min_num_containers, max_num_containers + 1):
        for comb in itertools.combinations(containers, n):
            if sum([c.volume for c in comb]) == target:
                options.add(tuple(comb))

    return len(options)


def part_2() -> Union[int, str]:
    containers = [Container(i, int(v.strip())) for i, v in enumerate(input_lines(_INPUT_PATH))]
    containers.sort(key=lambda x: x.volume)
    target = 150

    tot = 0
    for min_num_containers in range(1, len(containers)):
        tot += containers[-min_num_containers].volume
        if tot >= target:
            break
    else:
        min_num_containers = 1

    tot = 0
    for max_num_containers in range(len(containers)):
        tot += containers[max_num_containers].volume
        if tot >= target:
            break
    else:
        max_num_containers = len(containers)

    options = set()
    done = False
    for n in range(min_num_containers, max_num_containers + 1):
        for comb in itertools.combinations(containers, n):
            if sum([c.volume for c in comb]) == target:
                done = True
                options.add(tuple(comb))
        if done:
            break

    return len(options)


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
