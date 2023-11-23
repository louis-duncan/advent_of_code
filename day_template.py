from pathlib import Path
from typing import Union


def raw_input(input_path: Path = Path("input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read()
    return data.strip()


def part_1() -> Union[int, str]:
    ...


def part_2() -> Union[int, str]:
    ...


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("\nPart 2:", part_2())
