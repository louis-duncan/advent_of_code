import time
from typing import Union

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/2
"""

_INPUT_PATH = au.INPUT_PATH  # _TEST


def get_sections():
    _raw_input = au.raw_input(_INPUT_PATH)
    _sections = _raw_input.strip().split(",")
    for _s in _sections:
        _parts = _s.split("-")
        yield int(_parts[0]), int(_parts[1])


def part_1() -> Union[int, str]:
    sections: list[tuple[int, int]] = [s for s in get_sections()]
    bad_ids_sum = 0

    for s in sections:
        end_len = len(str(s[1]))
        if end_len % 2 == 1:
            end_len = end_len - 1

        for i in range(s[0], s[1] + 1):
            i_str = str(i)
            l_i_str = len(i_str)

            if len(i_str) % 2 == 1:
                continue
            elif len(i_str) > end_len:
                break

            half_i = int(l_i_str / 2)
            if i_str[:half_i] == i_str[half_i:]:
                bad_ids_sum += i

    return bad_ids_sum


def check(i_str, part_size, n) -> bool:
   return i_str.count(i_str[:part_size]) == n


def part_2() -> Union[int, str]:
    sections: list[tuple[int, int]] = [s for s in get_sections()]
    bad_ids_sum = 0

    for s in sections:
        for i in range(s[0], s[1] + 1):
            i_str = str(i)
            l_i_str = len(i_str)

            for size in (2, 3, 5, 7):
                if l_i_str % size == 0:
                    if check(i_str, l_i_str // size, size):
                        bad_ids_sum += i
                        break
    return bad_ids_sum


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
