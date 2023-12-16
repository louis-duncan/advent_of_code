import re
from pathlib import Path
from typing import Union, Iterator, Optional, Type, Any
import more_itertools as ir

"""
https://adventofcode.com/2023/day/9
"""


def raw_input(input_path: Union[Path, str] = Path("test_input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read()
    return data


def input_lines(
        input_path: Union[Path, str] = Path("test_input.txt"),
        convert_type: Optional[Type] = None
) -> Iterator[Any]:
    for line in raw_input(input_path).strip().split("\n"):
        if convert_type is None:
            yield line.strip()
        else:
            yield convert_type(line.strip())


def part_1() -> Union[int, str]:
    sequences: list[list[int]] = []
    for line in input_lines("input.txt"):
        sequences.append([int(n) for n in line.split(" ")])

    for sequence in sequences:
        derivatives: list[list[int]] = [sequence[-1:], ]

        while not (max(derivatives[-1]) == min(derivatives[-1]) == 0):
            # While no derivatives or last layer is not all 0s
            derivatives[0].insert(0, sequence[-(len(derivatives[0]) + 1)])
            derivatives.append([])
            for i in range(len(derivatives) - 1):
                derivatives[i + 1].insert(0, derivatives[i][1] - derivatives[i][0])

        new_value = 0
        for v in [t[-1] for t in reversed(derivatives)]:
            # Go through the last value in each sequence from bottom to top
            new_value = v + new_value

        sequence.append(new_value)

    return sum([s[-1] for s in sequences])


def part_2() -> Union[int, str]:
    sequences: list[list[int]] = []
    for line in input_lines("input.txt"):
        sequences.append(list(reversed([int(n) for n in line.split(" ")])))

    for sequence in sequences:
        derivatives: list[list[int]] = [sequence[-1:], ]

        while (len(derivatives) < 2) or (not (max(derivatives[-2]) == min(derivatives[-2]) == 0)):
            # While no derivatives or last layer is not all 0s
            derivatives[0].insert(0, sequence[-(len(derivatives[0]) + 1)])
            derivatives.append([])
            for i in range(len(derivatives) - 1):
                derivatives[i + 1].insert(0, derivatives[i][1] - derivatives[i][0])

        new_value = 0
        for v in [t[-1] for t in reversed(derivatives)]:
            # Go through the last value in each sequence from bottom to top
            new_value = v + new_value

        sequence.append(new_value)

    return sum([s[-1] for s in sequences])


if __name__ == "__main__":
    print("Part 1:", part_1())
    print()
    print("Part 2:", part_2())
