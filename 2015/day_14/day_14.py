import re
import time
from dataclasses import dataclass

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/14
"""

_INPUT_PATH = INPUT_PATH#_TEST


def part_1() -> Union[int, str]:
    end_secs = 2503
    distances = {}
    for line in input_lines(_INPUT_PATH):
        name, speed_str, flight_time_str, rest_time_str = re.match(
            r"(\w+) can fly (\d+) km/s for (\d+) seconds.* (\d+) seconds",
            line
        ).groups()
        speed = int(speed_str)
        flight_time = int(flight_time_str)
        rest_time = int(rest_time_str)

        n = end_secs // (flight_time + rest_time)
        distance = n * speed * flight_time
        remaining_time = end_secs - ((flight_time + rest_time) * n)
        distance += min(remaining_time, flight_time) * speed
        distances[name] = distance

    return max(distances.values())


def part_2() -> Union[int, str]:
    @dataclass
    class Reindeer:
        name: str
        speed: int
        flight_time: int
        rest_time: int
        distance: int = 0
        resting: bool = False
        time_since_last_change: int = 0

        def tick(self):
            if not self.resting:
                self.distance += self.speed

            self.time_since_last_change += 1
            wait_time = self.rest_time if self.resting else self.flight_time
            if self.time_since_last_change == wait_time:
                self.resting = not self.resting
                self.time_since_last_change = 0

    reindeers: list[Reindeer] = []

    for line in input_lines(_INPUT_PATH):
        name, speed_str, flight_time_str, rest_time_str = re.match(
            r"(\w+) can fly (\d+) km/s for (\d+) seconds.* (\d+) seconds",
            line
        ).groups()
        speed = int(speed_str)
        flight_time = int(flight_time_str)
        rest_time = int(rest_time_str)
        reindeers.append(Reindeer(name, speed, flight_time, rest_time))

    scores: dict[str, int] = {r.name: 0 for r in reindeers}
    for _ in range(2503):
        furthest = 0
        for r in reindeers:
            r.tick()
            if r.distance > furthest:
                furthest = r.distance

        for r in reindeers:
            if r.distance == furthest:
                scores[r.name] += 1

    return max(scores.values())


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
