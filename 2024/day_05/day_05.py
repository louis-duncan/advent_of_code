import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/5
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    rules: dict[int, list[int]] = {}
    flags: dict[int, bool] = {}
    lines = list(input_lines(_INPUT_PATH))
    rules_section, pages_section = lines[:lines.index("")], lines[lines.index("") + 1:]
    for rule_line in rules_section:
        a_str, b_str = rule_line.split("|")
        a, b = int(a_str), int(b_str)
        if b not in rules:
            rules[b] = []
        rules[b].append(a)
        flags[a] = False
    page_nums_lists: list[list[int]] = []
    for pages_line in pages_section:
        page_nums_lists.append(
            [int(n_str) for n_str in pages_line.split(",")]
        )


    result = 0

    for page_nums in page_nums_lists:
        # Reset flags
        for f in flags:
            flags[f] = False

        valid = True
        for n in page_nums:
            if n in rules:
                for required in rules[n]:
                    if required in page_nums and not flags[required]:
                        valid = False
                        break
            if not valid:
                break
            flags[n] = True

        if valid:
            result += page_nums[len(page_nums) // 2]

    return result


def part_2() -> Union[int, str]:
    rules: dict[int, set[int]] = {}
    flags: dict[int, bool] = {}
    lines = list(input_lines(_INPUT_PATH))
    rules_section, pages_section = lines[:lines.index("")], lines[lines.index("") + 1:]
    for rule_line in rules_section:
        a_str, b_str = rule_line.split("|")
        a, b = int(a_str), int(b_str)
        if b not in rules:
            rules[b] = set()
        rules[b].add(a)
        flags[a] = False
    page_nums_lists: list[list[int]] = []
    for pages_line in pages_section:
        page_nums_lists.append(
            [int(n_str) for n_str in pages_line.split(",")]
        )

    incorrect_updates: list[list[int]] = []

    for page_nums in page_nums_lists:
        # Reset flags
        for f in flags:
            flags[f] = False

        valid = True
        for n in page_nums:
            if n in rules:
                for required in rules[n]:
                    if required in page_nums and not flags[required]:
                        valid = False
                        break
            if not valid:
                break
            flags[n] = True

        if not valid:
            incorrect_updates.append(page_nums)

    def find_candidate(_page: list[int]) -> int:
        for _n in _page:
            if min([flags[r] for r in rules.get(_n, set())] + [True]):
                return _n
        else:
            raise ValueError("No candidate")

    result = 0
    for start_order in incorrect_updates:
        # Reset flags
        for f in flags:
            flags[f] = not f in start_order
        new_order = []
        for _ in range(len(start_order)):
            next_num = find_candidate(start_order)
            new_order.append(next_num)
            start_order.remove(next_num)
            flags[next_num] = True
        result += new_order[len(new_order) // 2]

    return result


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
