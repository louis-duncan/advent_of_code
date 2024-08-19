import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/6
"""

class Region:
    def __init__(self, command: str, start_xy: tuple[int, int], end_xy: tuple[int, int]):
        self.command = command
        self.start_x, self.start_y = start_xy
        self.end_x, self.end_y = end_xy

    def __contains__(self, point: tuple[int, int]) -> bool:
        return self.start_x <= point[0] <= self.end_x and self.start_y <= point[1] <= self.end_y


def part_1() -> Union[int, str]:
    regions: list[Region] = []
    for line in input_lines("input.txt"):
        try:
            command = re.search(r"^[a-z ]+(?= \d)", line).group()
            start_x, start_y, end_x, end_y = [int(v) for v in re.findall(r"\d+", line)]
            regions.append(
                Region(
                    command=command,
                    start_xy=(start_x, start_y),
                    end_xy=(end_x, end_y)
                )
            )
        except Exception as e:
            print(f"Regex failed on line: {line}")
            raise e

    on_count = 0
    for x in range(1000):
        print(x)
        for y in range(1000):
            state = False
            for region in regions:
                if (x, y) in region:
                    if region.command == "turn on":
                        state = True
                    elif region.command == "turn off":
                        state = False
                    elif region.command == "toggle":
                        state = not state
                    else:
                        raise ValueError(f"Unknown command '{region.command}'")
            on_count += int(state)
    return on_count

def part_2() -> Union[int, str]:
    regions: list[Region] = []
    for line in input_lines("input.txt"):
        try:
            command = re.search(r"^[a-z ]+(?= \d)", line).group()
            start_x, start_y, end_x, end_y = [int(v) for v in re.findall(r"\d+", line)]
            regions.append(
                Region(
                    command=command,
                    start_xy=(start_x, start_y),
                    end_xy=(end_x, end_y)
                )
            )
        except Exception as e:
            print(f"Regex failed on line: {line}")
            raise e

    total = 0
    for x in range(1000):
        print(x)
        for y in range(1000):
            state = 0
            for region in regions:
                if (x, y) in region:
                    if region.command == "turn on":
                        state += 1
                    elif region.command == "turn off":
                        state -= 1
                        if state < 0:
                            state = 0
                    elif region.command == "toggle":
                        state += 2
                    else:
                        raise ValueError(f"Unknown command '{region.command}'")
            total += state
    return total


if __name__ == "__main__":
    p1_start = time.time()
    part_1_answer = None  # part_1()
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
