from pathlib import Path
from typing import Union, Iterator


def raw_input(input_path: Path = Path("input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read()
    return data


def input_lines(input_path: Path = Path("input.txt")) -> Iterator[str]:
    for line in raw_input(input_path).strip().split("\n"):
        yield line.strip()


def part_1() -> Union[int, str]:
    ...


def part_2() -> Union[int, str]:
    ...


if __name__ == "__main__":
    print("Part 1:", part_1())
    print()
    print("Part 2:", part_2())
