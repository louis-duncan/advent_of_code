import re
from math import inf
from pathlib import Path
from typing import Union, Iterator, Optional, Type, Any

"""
https://adventofcode.com/2023/day/5
"""


class Range:
    def __init__(self, start: int, size: int):
        self.start = start
        self.size = size

    @property
    def end(self):
        return self.start + self.size - 1

    def overlaps(self, other: 'Range'):
        if other.start <= self.start <= other.end:
            return True
        if other.start <= self.end <= other.end:
            return True
        if self.start <= other.start <= self.end:
            return True
        if self.start <= other.end <= self.end:
            return True
        return False

    def __hash__(self):
        return hash((self.start, self.size))

    def __eq__(self, other):
        if isinstance(other, Range):
            return self.start == other.start and self.size == other.size
        else:
            return False

    def __repr__(self):
        return f"Range(start={self.start}, end={self.end}, size={self.size})"

    def __add__(self, other: 'Range') -> 'Range':
        if not isinstance(other, Range):
            raise TypeError(f"Cannot add type {type(other)} to type Range")

        if not self.overlaps(other):
            raise ValueError(f"Cannot add non-overlapping Ranges")

        new_start = min(self.start, other.start)
        new_end = max(self.end, other.end)
        new_size = (new_end - new_start) + 1

        return Range(new_start, new_size)

    def __sub__(self, other: 'Range') -> list['Range']:
        if not self.overlaps(other):
            return [self]

        if other.start <= self.start and other.end >= self.end:
            # other subsumes self, so ranges
            return []
        elif other.start > self.start and other.end < self.end:
            # other is entirely inside self, return two ranges.
            range_1 = Range(self.start, other.start - self.start)
            range_2 = Range(other.end + 1, self.end - other.end)
            return [range_1, range_2]
        elif other.start > self.start:
            # other starts inside self, but ends after
            return [Range(self.start, other.start - self.start)]
        elif other.end < self.end:
            # other starts outside self, but ends inside
            return [Range(other.end + 1, self.end - other.end)]

    def intersect(self, other: 'Range') -> Optional['Range']:
        if self.overlaps(other):
            new_start = max(self.start, other.start)
            new_end = min(self.end, other.end)
            return Range(new_start, new_end + 1 - new_start)
        else:
            return None


class Mapping:
    def __init__(self, start_1: int, start_2: int, size: int):
        self.start_1 = start_1
        self.start_2 = start_2
        self.size = size
        self.range_1 = Range(self.start_1, size)

    def map(self, value: int) -> Optional[int]:
        if not (self.start_1 <= value <= self.start_1 + (self.size - 1)):
            return None
        return self.start_2 + (value - self.start_1)

    def reverse_map(self, value: int) -> Optional[int]:
        if not (self.start_2 <= value <= self.start_2 + (self.size - 1)):
            return None
        return self.start_1 + (value - self.start_2)

    def map_range(self, value: Range) -> list[Range]:
        result_ranges = value - self.range_1
        intersection = self.range_1.intersect(value)
        if intersection is not None:
            intersection.start = self.start_2
            result = intersection
            for i in range(len(result_ranges)):
                if result_ranges[i].overlaps(result):
                    result_ranges[i] = result_ranges[i] + result
            else:
                result_ranges.append(result)
        return result_ranges

    def __repr__(self):
        return f"Mapping(start_1={self.start_1}, start_2={self.start_2}, size={self.size})"


class MappingSet:
    def __init__(self, name: str, maps: list[Mapping]):
        self.name = name
        self.maps = maps

    def map(self, value: int, reverse=False) -> int:
        for mapping in self.maps:
            if reverse:
                mapped_value = mapping.reverse_map(value)
            else:
                mapped_value = mapping.map(value)
            if mapped_value:
                return mapped_value
        else:
            return value

    def reverse_map(self, value: int) -> int:
        return self.map(value, reverse=True)

    def map_range(self, value: Range) -> list[Range]:
        result_ranges = []
        for mapping in self.maps:
            for nr in mapping.map_range(value):
                result_ranges.append(nr)
        return collapse_ranges(result_ranges)

    def __repr__(self):
        return f"MappingSet(name={repr(self.name)})"


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
    input_text = raw_input("input.txt")
    input_text = input_text.replace("\r", "")
    seeds = [int(s) for s in re.search(r"(?<=seeds: )(\d+ ?)+", input_text).group().split(" ")]
    blocks = re.findall(r"(?<=\n\n).*?(?=\n\n|$)", input_text, flags=re.DOTALL)

    mappings: dict[str, MappingSet] = {}
    ordered_mappings: list[MappingSet] = []
    for block in blocks:
        block_lines = block.strip().split("\n")
        name = block_lines[0].strip().split(" ")[0]
        maps: list[Mapping] = []
        for line in block_lines[1:]:
            start_2, start_1, size = [int(v) for v in line.strip().split(" ")]
            new_map = Mapping(start_1, start_2, size)
            maps.append(new_map)
        mappings[name] = (MappingSet(name, maps))
        ordered_mappings.append(mappings[name])

    locations: list[int] = []
    for seed in seeds:
        value = seed
        for mapping in ordered_mappings:
            value = mapping.map(value)
        locations.append(value)

    return min(locations)


def range_test():
    r = Range(20, 100)
    s1 = Range(40, 3)
    print(r, "-", s1)
    res = r - s1
    print(res)
    print()
    s2 = Range(90, 30)
    print(r, "-", s2)
    res = r - s2
    print(res)
    print()
    s3 = Range(1, 30)
    print(r, "-", s3)
    res = r - s3
    print(res)
    print()
    s4 = Range(1, 110)
    print(r, "-", s4)
    res = r - s4
    print(res)
    print()
    s5 = Range(80, 100)
    print(r, "intersect", s5)
    res = r.intersect(s5)
    print(res)

    print()
    m = Mapping(50, 60, 2)
    print(m)
    print(r, "mapped", m.map_range(r))

    print()
    r2 = Range(140, 10)
    r3 = Range(200, 12)
    r4 = Range(100, 42)
    print(r, r2, r3, r4)
    print("collapsed", collapse_ranges([r, r2, r3, r4]))


def collapse_ranges(ranges: list[Range]) -> list[Range]:
    input_ranges = list(ranges)

    changed = True
    while changed:
        start_len = len(input_ranges)

        merged = False
        for i in range(len(input_ranges)):
            for j in range(i + 1, len(input_ranges)):
                if input_ranges[i].overlaps(input_ranges[j]):
                    input_ranges[j] = input_ranges[i] + input_ranges[j]
                    input_ranges.pop(0)
                    merged = True
                    break
            if merged:
                break

        changed = len(input_ranges) != start_len

    return input_ranges


def part_2() -> Union[int, str]:
    input_text = raw_input("test_input.txt")
    input_text = input_text.replace("\r", "")
    seed_ranges = []
    seed_numbers = [int(s) for s in re.search(r"(?<=seeds: )(\d+ ?)+", input_text).group().split(" ")]
    for i in range(0, len(seed_numbers), 2):
        seed_ranges.append(Range(seed_numbers[i], seed_numbers[i + 1]))
    blocks = re.findall(r"(?<=\n\n).*?(?=\n\n|$)", input_text, flags=re.DOTALL)

    mappings: dict[str, MappingSet] = {}
    ordered_mappings: list[MappingSet] = []
    for block in blocks:
        block_lines = block.strip().split("\n")
        name = block_lines[0].strip().split(" ")[0]
        maps: list[Mapping] = []
        for line in block_lines[1:]:
            start_2, start_1, size = [int(v) for v in line.strip().split(" ")]
            new_map = Mapping(start_1, start_2, size)
            maps.append(new_map)
        mappings[name] = (MappingSet(name, maps))
        ordered_mappings.append(mappings[name])

    results: dict[Range, list[Range]] = {}
    for seed_range in seed_ranges:
        current_ranges = [seed_range]
        for mapping in ordered_mappings:
            new_ranges: list[Range] = []
            for current_range in current_ranges:
                for new_range in mapping.map_range(current_range):
                    new_ranges.append(new_range)
            collapsed_ranges = collapse_ranges(new_ranges)
            current_ranges = collapsed_ranges
        results[seed_range] = list(current_ranges)

    lowest = inf
    for result_ranges in results.values():
        for result_range in result_ranges:
            if result_range.start < lowest:
                lowest = result_range.start

    return lowest


if __name__ == "__main__":
    print("Part 1:", part_1())
    print()
    #range_test()
    print("Part 2:", part_2())
