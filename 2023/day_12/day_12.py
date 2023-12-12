from aoc_utils import *
from itertools import permutations

import pyperclip

"""
https://adventofcode.com/2023/day/12
"""


def part_1() -> Union[int, str]:
    counts: list[int] = []
    for line in input_lines("input.txt"):
        option_count = 0
        template, numbers = line.split(" ")
        numbers = [int(n) for n in numbers.split(",")]
        num_unknown = template.count("?")
        num_known_broken = template.count("#")
        num_expected_broken = sum(numbers)
        num_broken_to_find = num_expected_broken - num_known_broken
        num_fixed_to_find = num_unknown - num_broken_to_find
        tried: set[list[str]] = set()
        for p in permutations((num_broken_to_find * "#") + (num_fixed_to_find * ".")):
            if p in tried:
                continue
            test: str = template
            for c in p:
                test = test.replace("?", c, 1)
            lengths = [len(part) for part in test.split(".") if len(part) > 0]
            if lengths == numbers:
                option_count += 1
            tried.add(p)
        counts.append(option_count)
    with open("p1_out.txt", "w") as fh:
        fh.write("\n".join([str(c) + "\n" for c in counts]))
    return sum(counts)


def part_2() -> Union[int, str]:
    ...


if __name__ == "__main__":
    part_1_answer = part_1()
    if part_1_answer is not None:
        print("Part 1:", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    part_2_answer = part_2()
    if part_2_answer is not None:
        print("Part 2:", part_2_answer)
        pyperclip.copy(part_2_answer)
