import dataclasses
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2017/day/9
"""

_INPUT_PATH = INPUT_PATH  # _TEST


@dataclasses.dataclass
class Group:
    parent: Optional['Group'] = None
    children: list['Group'] = dataclasses.field(default_factory=list)
    _score: Optional[int] = None
    garbage_count = 0

    @property
    def score(self) -> int:
        if self._score is not None:
            return self._score
        else:
            return self.parent.score + 1

    @property
    def total_score(self) -> int:
        return sum((c.total_score for c in self.children)) + self.score

    @property
    def total_garbage_count(self) -> int:
        return sum((c.total_garbage_count for c in self.children)) + self.garbage_count

    def __str__(self):
        return "{" + str(self.score) + ",".join([str(c) for c in self.children]) + "}"


def stream_to_group(stream: str, start_pos: int) -> tuple[Group, int]:
    assert stream[start_pos] == "{"
    pos = start_pos + 1
    new_group = Group()

    in_garbage = False
    while True:
        char = stream[pos]
        if char == "!":
            pos += 1
        elif not in_garbage:
            if char == "}":
                return new_group, pos
            elif char == "<":
                in_garbage = True
            elif char == "{":
                new_child, pos = stream_to_group(stream, pos)
                new_child.parent = new_group
                new_group.children.append(new_child)
        else:
            if char == ">":
                in_garbage = False
            else:
                new_group.garbage_count += 1

        pos += 1


def part_1() -> Union[int, str]:
    stream: str = raw_input(_INPUT_PATH).strip()

    root, _ = stream_to_group(stream, 0)
    root._score = 1

    return root.total_score


def part_2() -> Union[int, str]:
    stream: str = raw_input(_INPUT_PATH).strip()

    root, _ = stream_to_group(stream, 0)

    return root.total_garbage_count


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
