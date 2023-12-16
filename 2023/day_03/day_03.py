from __future__ import annotations
from pathlib import Path
from typing import Union, Iterator, Optional, Type, Any


"""
https://adventofcode.com/2023/day/3
"""


def raw_input(input_path: Path = Path("input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read()
    return data


def input_lines(input_path: Path = Path("input.txt"), convert_type: Optional[Type] = None) -> Iterator[Any]:
    for line in raw_input(input_path).strip().split("\n"):
        if convert_type is None:
            yield line.strip()
        else:
            yield convert_type(line.strip())


def get_whole_number(grid: list[list[str]], x, y) -> (int, tuple[int, int]):
    assert grid[y][x].isdigit()

    start_found = x <= 0
    while not start_found:
        if x == 0:
            start_found = True
        elif grid[y][x-1].isdigit():
            x -= 1
        else:
            start_found = True
    start_pos = x

    digits = ""
    done = False
    while not done:
        if x >= len(grid[y]):
            done = True
        elif not grid[y][x].isdigit():
            done = True
        else:
            digits += grid[y][x]
            x += 1

    return (start_pos, y), int(digits)


def find_numbers(grid: list[list[str]], x, y) -> set[tuple[tuple[int, int], int]]:
    numbers = set()
    for y_ in (y - 1, y, y + 1):
        for x_ in (x - 1, x, x + 1):
            if y_ < 0 or y_ >= len(grid):
                pass
            elif x_ < 0 or x_ >= len(grid):
                pass
            elif x_ == x and y_ == y:
                pass
            else:
                if grid[y_][x_].isdigit():
                    numbers.add(get_whole_number(grid, x_, y_))
    return numbers


def part_1() -> Union[int, str]:
    grid: list[list[str]] = []

    number_chars = "1234567890"

    symbols = set()

    for line in input_lines(Path("input.txt")):
        grid.append(line)
        for c in line:
            if c != "." and c not in number_chars:
                symbols.add(c)

    parts_numbers: dict[tuple[int, int], dict[str, Union[int, set[tuple[int, int]]]]] = {}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in symbols:
                for new_pos, new_value in find_numbers(grid, x, y):
                    if new_pos in parts_numbers:
                        assert parts_numbers[new_pos]['value'] == new_value
                        if (x, y) not in parts_numbers[new_pos]['symbols']:
                            parts_numbers[new_pos]['symbols'].add((x, y))
                    else:
                        parts_numbers[new_pos] = {
                            'value': new_value,
                            'symbols': {(x, y), }
                        }
    return sum([pn['value'] for pn in parts_numbers.values()])


def part_2() -> Union[int, str]:
    grid: list[list[str]] = []

    number_chars = "1234567890"

    symbols = set()

    for line in input_lines(Path("input.txt")):
        grid.append(line)
        for c in line:
            if c != "." and c not in number_chars:
                symbols.add(c)

    parts_numbers: dict[tuple[int, int], dict[str, Union[int, set[tuple[int, int]]]]] = {}
    gears: set[tuple[int, int]] = set()

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in symbols:
                if grid[y][x] == "*":
                    gears.add((x, y))
                for new_pos, new_value in find_numbers(grid, x, y):
                    if new_pos in parts_numbers:
                        assert parts_numbers[new_pos]['value'] == new_value
                        if (x, y) not in parts_numbers[new_pos]['symbols']:
                            parts_numbers[new_pos]['symbols'].add((x, y))
                    else:
                        parts_numbers[new_pos] = {
                            'value': new_value,
                            'symbols': {(x, y), }
                        }

    ratios: list[int] = []
    for gear in gears:
        values = [pn['value'] for pn in parts_numbers.values() if gear in pn['symbols']]
        if len(values) == 2:
            ratios.append(values[0] * values[1])

    return sum(ratios)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print()
    print("Part 2:", part_2())
