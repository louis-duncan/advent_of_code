import dataclasses
import re
import time
from math import inf
from turtledemo.penrose import inflatedart
from typing import Union

import pyperclip

import aoc_utils as au


"""
https://adventofcode.com/2025/day/10
"""

_INPUT_PATH = au.INPUT_PATH_TEST


def print_state(state: int, num_lights: int):
    s = bin(state).split("b")[1].zfill(num_lights)
    s = s.replace("0", ".").replace("1", "#")
    print(f"[{s}]")


def part_1() -> Union[int, str]:
    total = 0
    for line in au.input_lines(test=False):
        target_pattern = re.match(r"\[([.#]+)]", line).groups()[0]
        state = int(target_pattern.replace("#", "1").replace(".", "0"), 2)
        num_lights = len(target_pattern)
        buttons: list[int] = []
        for buttons_str in re.findall(r"(\(\d(?:,\d+)*\))", line):
            values: tuple[int, ...] = eval(buttons_str)
            if isinstance(values, int):
                values = (values,)
            button_val_str = ""
            for i in range(len(target_pattern)):
                n = "1" if i in values else "0"
                button_val_str += n
            buttons.append(int(button_val_str, 2))

        seen_states: set[int] = set()
        current_states: set[int] = {state}
        depth = 0
        done = False
        prev = -1
        while not done:
            depth += 1
            new_states = set()
            for state in current_states:
                for button in buttons:
                    if button == prev:
                        continue
                    new_state = state ^ button
                    if new_state == 0:
                        done = True
                    if new_state not in seen_states:
                        seen_states.add(new_state)
                        new_states.add(new_state)
            current_states = new_states

        total += depth

    return total


def part_2() -> Union[int, str]:
    total = 0
    for line in au.input_lines(test=False):
        target_pattern = re.match(r"\[([.#]+)]", line).groups()[0]
        state = int(target_pattern.replace("#", "1").replace(".", "0"), 2)
        num_lights = len(target_pattern)
        buttons: list[int] = []
        for buttons_str in re.findall(r"(\(\d(?:,\d+)*\))", line):
            values: tuple[int, ...] = eval(buttons_str)
            if isinstance(values, int):
                values = (values,)
            button_val_str = ""
            for i in range(len(target_pattern)):
                n = "1" if i in values else "0"
                button_val_str += n
            buttons.append(int(button_val_str, 2))

        seen_states: set[int] = set()
        current_states: set[int] = {state}
        depth = 0
        done = False
        prev = -1
        while not done:
            depth += 1
            new_states = set()
            for state in current_states:
                for button in buttons:
                    if button == prev:
                        continue
                    new_state = state ^ button
                    if new_state == 0:
                        done = True
                    if new_state not in seen_states:
                        seen_states.add(new_state)
                        new_states.add(new_state)
            current_states = new_states

        total += depth

    return total


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
