import re
import time
from re import Pattern

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/19
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    replacements: dict[str, list[str]] = {}
    lines = list(input_lines(_INPUT_PATH))
    for line in lines[:-2]:
        a, b = line.strip().split(" => ")
        if a not in replacements:
            replacements[a] = []
        replacements[a].append(b)
    molecule_str = lines[-1].strip()

    results = set()
    for i in range(len(molecule_str)):
        if molecule_str[i] in replacements:
            mol = molecule_str[i]
        elif molecule_str[i: i+2] in replacements:
            mol = molecule_str[i: i+2]
        else:
            continue

        for replacement in replacements[mol]:
            new = molecule_str[:i] + replacement + molecule_str[i + len(mol):]
            results.add(new)

    return len(results)


def sub(text: str, pos: int, old: str, new: str) -> str:
    return text[:pos] + new + text[pos + len(old):]


def part_2_old() -> Union[int, str]:
    replacements: dict[str, str] = {}
    patterns: dict[str, Pattern] = {}
    lines = list(input_lines(_INPUT_PATH))
    for line in lines[:-2]:
        a, b = line.strip().split(" => ")
        patterns[b] = re.compile(b)
        replacements[b] = a
    target = lines[-1].strip()

    seen_before = {target,}
    options = {target,}
    num_steps = 0
    done = False
    while not done:
        num_steps += 1
        molecule_strings = options.copy()
        options.clear()
        for molecule_str in molecule_strings:
            for mol, pattern in patterns.items():
                for match in pattern.finditer(molecule_str):
                    new = sub(molecule_str, match.start(), mol, replacements[mol])
                    if new == "e":
                        return num_steps
                    if new in seen_before:
                        pass
                    else:
                        options.add(new)
                        seen_before.add(new)


def part_2() -> Union[int, str]:
    replacements: dict[str, str] = {}
    patterns: dict[str, Pattern] = {}
    lines = list(input_lines(_INPUT_PATH))
    for line in lines[:-2]:
        a, b = line.strip().split(" => ")
        patterns[b] = re.compile(b)
        replacements[b] = a
    molecule = lines[-1].strip()

    steps = 0
    stuck = False
    while True:
        stuck = True
        for mol, pattern in patterns.items():
            for match in pattern.finditer(molecule):
                stuck = False
                steps += 1
                molecule = sub(molecule, match.start(), mol, replacements[mol])
                if molecule == "e":
                    return steps
        if stuck:
            raise Exception(f"Got stuck: {molecule}")


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
