from pathlib import Path
from typing import Union, Iterator, Optional, Type, Any

"""
https://adventofcode.com/2020/day/9
"""


class Buffer:
    BUFFER_SIZE = 25
    input_order: list[int] = []
    value_order: list[int] = []
    buffer_filled = False

    @classmethod
    def add_number(cls, new_value: int) -> bool:
        is_valid = cls._is_new_number_valid(new_value)

        cls.input_order.append(new_value)

        if len(cls.input_order) > cls.BUFFER_SIZE:
            removed = cls.input_order.pop(0)
            cls.value_order.remove(removed)

        if len(cls.value_order) == 0:
            cls.value_order.append(new_value)

        else:
            for i, number in enumerate(cls.value_order):
                if new_value <= number:
                    cls.value_order.insert(i, new_value)
                    break
            else:
                cls.value_order.append(new_value)

        assert len(cls.input_order) == len(cls.value_order)
        assert len(cls.input_order) <= cls.BUFFER_SIZE

        if not cls.buffer_filled:
            if len(cls.input_order) == cls.BUFFER_SIZE:
                cls.buffer_filled = True
            return True
        else:
            return is_valid

    @classmethod
    def _is_new_number_valid(cls, value) -> bool:
        half = value / 2
        for num in cls.input_order:
            remainder = value - num
            if (remainder in cls.input_order) and (remainder != half):
                return True
        else:
            return False


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


def part_1() -> Union[int, str]:
    line_gen = input_lines()

    for _, line in zip(range(Buffer.BUFFER_SIZE), line_gen):
        value = int(line)
        Buffer.add_number(value)

    print("buffer full")

    for line in line_gen:
        value = int(line)
        valid = Buffer.add_number(value)
        if not valid:
            return value


def part_2(target: int) -> Union[int, str]:
    lines: list[int] = list(input_lines(convert_type=int))

    start = 0
    end = 1
    total = lines[start] + lines[end]

    while total != target:
        if total > target:
            start += 1
            if start == end:
                end += 1
        elif total < target:
            end += 1
        total = sum(lines[start:end+1])

    print(start, end)
    return min(lines[start:end+1]) + max(lines[start:end+1])


if __name__ == "__main__":
    part_1_result = part_1()
    assert isinstance(part_1_result, int)
    print("Part 1:", part_1_result)
    print()
    print("Part 2:", part_2(part_1_result))
