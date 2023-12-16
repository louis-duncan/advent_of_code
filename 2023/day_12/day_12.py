from aoc_utils import *
from itertools import permutations
from functools import cache

import pyperclip

"""
https://adventofcode.com/2023/day/12
"""

def can_fit(num: int, pattern: str, pos: int) -> bool:
    if pos > 0 and pattern[pos - 1] == "#":
        return False

    section = pattern[pos: pos + num]
    if "." in section:
        return False

    try:
        if pattern[pos + num] == "#":
            return False
    except IndexError:
        pass

    return True

@cache
def drop_in(num: int, pattern: str, pos: int) -> str:
    start_len = len(pattern)
    if len(pattern) == num:
        assert pos == 0
        return "#" * num
    elif pos == 0:
        new = (num * "#") + "." + pattern[pos + num + 1:]
    elif pos + num == len(pattern):
        new = pattern[:pos - 1] + "." + (num * "#")
    else:
        new = pattern[:pos - 1] + "." + (num * "#") + "." + pattern[pos + num + 1:]
    if len(new) != start_len:
        print("num={}, pattern={}, pos={}".format(num, pattern, pos))
        print("out:", new)
        assert len(new) == start_len
    return new

@cache
def find_options(pattern: str, numbers: tuple[int, ...]) -> set[str]:
    pos = 0
    space_for_others = sum(numbers[1:]) + len(numbers[1:]) - 1
    max_pos = len(pattern) - (space_for_others + numbers[0])

    new_patterns: set[str] = set()

    for i in range(pos, max_pos):
        if can_fit(numbers[0], pattern, i):
            changed_pattern = drop_in(numbers[0], pattern, i)
            if len(numbers) > 1:
                recursive_new = find_options(changed_pattern[i + numbers[0] + 1:], numbers[1:])
                if recursive_new is None:
                    continue
                for new in recursive_new:
                    to_add = (changed_pattern[:i + numbers[0] + 1] + new).replace("?", ".")
                    assert len(to_add) == len(pattern)
                    if len([0 for _ in to_add.split(".") if _]) == len(numbers):
                        new_patterns.add(to_add)
            else:
                new_patterns.add(changed_pattern)
    return new_patterns


def tests():
    pattern = ".?.?..?????.?#"
    assert can_fit(3, pattern, 5) is False
    assert can_fit(3, pattern, 6) is True
    assert can_fit(3, pattern, 7) is True
    assert can_fit(3, pattern, 8) is True
    assert can_fit(3, pattern, 9) is False

    pattern = ".?.?..????#.?#"
    assert can_fit(3, pattern, 5) is False
    assert can_fit(3, pattern, 6) is True
    assert can_fit(3, pattern, 7) is False
    assert can_fit(3, pattern, 8) is True
    assert can_fit(3, pattern, 9) is False
    assert can_fit(6, '#?#?#?#?', 0) is True

    assert drop_in(3, "#?#?#?#?#?#?#?#",  0) == "###.#?#?#?#?#?#"
    assert drop_in(3, "#?#?#?#?#?#?#?#",  4) == "#?#.###.#?#?#?#"
    assert drop_in(3, "#?#?#?#?#?#?#?#", 12) == "#?#?#?#?#?#.###"

    assert len(find_options("???.###", (1, 1, 3))) == 1
    assert len(find_options(".??..??...?##.", (1, 1, 3))) == 4
    exit()


def part_1() -> Union[int, str]:
    counts: list[int] = []
    i = 0
    for line in input_lines("input.txt"):
        symbols, numbers = line.split(" ")
        numbers = tuple([int(n) for n in numbers.split(",")])
        options = find_options(symbols, numbers)
        counts.append(len(options))
        #print(line)
        #for o in options: print("\t", o)
        #i += 1
        #if i == 10:
        #    break
    #print(counts)
    return sum(counts)


def part_2() -> Union[int, str]:
    counts: list[int] = []

    for i, line in enumerate(input_lines("input.txt")):
        symbols, numbers = line.split(" ")
        symbols = "?".join([symbols for _ in range(5)])
        numbers = ",".join([numbers for _ in range(5)])
        numbers = tuple([int(n) for n in numbers.split(",")])
        options = find_options(symbols, numbers)
        counts.append(len(options))
        if i % 100 == 0:
            print(i)
    output_file = Path("part2.txt")
    output_file.write_text(str(sum(counts)))
    return sum(counts)


if __name__ == "__main__":
    #tests()

    part_1_answer = part_1()
    if part_1_answer is not None:
        print("Part 1:", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    part_2_answer = part_2()
    if part_2_answer is not None:
        print("Part 2:", part_2_answer)
        pyperclip.copy(part_2_answer)
