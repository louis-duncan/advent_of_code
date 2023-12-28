import operator
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2023/day/24
"""


class Line2D:
    def __init__(self, name: str, x: int, y: int, dx: int, dy: int):
        self.name = name
        self.dx = dx
        self.dy = dy
        self.a = x
        self.b = y

    def __repr__(self):
        return f'Line2D(name={self.name}, a={self.a}, b={self.b})'

    @property
    def m(self) -> float:
        return self.dy / self.dx

    @property
    def c(self) -> float:
        return -(self.m * self.a) + self.b


def get_2d_line(
        name: str,
        coord: tuple[int, int, int],
        vector: tuple[int, int, int]
) -> Line2D:
    return Line2D(name, coord[0], coord[1], vector[0], vector[1])


def get_2d_intercept(line_1: Line2D, line_2: Line2D) -> Optional[tuple[float, float]]:
    if line_1.m == line_2.m:
        return None
    x = (line_1.c - line_2.c) / (line_2.m - line_1.m)
    y = (line_1.m * x) + line_1.c
    return x, y


def int_to_name(i: int) -> str:
    name = ""
    done = False
    while not done:
        name = chr(ord('A') + (i % 26)) + name
        i = i - (i % 26)
        i = (i // 26) - 1
        done = i < 0
    return name


def part_1() -> Union[int, str]:
    lines: list[Line2D] = []
    for i, line in enumerate(input_lines("input.txt")):
        coord_str, vector_str = line.split(" @ ")
        x_str, y_str, z_str = coord_str.split(", ")
        dx_str, dy_str, dz_str = vector_str.split(", ")
        coord = (int(x_str), int(y_str), int(z_str))
        vector = (int(dx_str), int(dy_str), int(dz_str))
        lines.append(get_2d_line(int_to_name(i), coord, vector))

    coord_min = 200000000000000
    coord_max = 400000000000000

    intercept_count = 0

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            intercept = get_2d_intercept(lines[i], lines[j])
            if intercept is not None:
                x, y = intercept
                if coord_min <= x <= coord_max and coord_min <= y <= coord_max:
                    if sign(lines[i].dx) == 1:
                        i_op = operator.ge
                    else:
                        i_op = operator.le
                    if sign(lines[j].dx) == 1:
                        j_op = operator.ge
                    else:
                        j_op = operator.le

                    if i_op(x, lines[i].a) and j_op(x, lines[j].a):
                        # print(f"Intercept found between {lines[i]} and {lines[j]} at {x}, {y}")
                        intercept_count += 1

    return intercept_count


def part_2() -> Union[int, str]:
    ...


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
