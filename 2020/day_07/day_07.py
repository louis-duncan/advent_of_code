import re
from pathlib import Path
from typing import Union


bags: dict[str, dict[str, Union[list[str], dict[str, int]]]] = {}


def raw_input(input_path: Path = Path("input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read().strip()
    return data.strip()


def load_bags():
    global bags

    for line in raw_input().split("\n"):
        """muted tomato bags contain 1 bright brown bag, 1 dotted gold bag, 2 faded gray bags, 1 posh yellow bag."""
        """dotted black bags contain no other bags."""
        bag_colour = re.match("(.*)(?= bags contain)", line).group()
        if bag_colour not in bags:
            bags[bag_colour] = {
                'can_contain': {},
                'can_be_contained_by': []
            }

        can_contain_colour_parts: list[str] = re.findall(r"(\d+.*?)(?=[,.])", line)
        for contain_part in can_contain_colour_parts:
            num, colour_name_part = contain_part.split(" ", 1)
            colour_name, _ = colour_name_part.rsplit(" ", 1)
            num = int(num)

            if colour_name not in bags:
                bags[colour_name] = {
                    'can_contain': {},
                    'can_be_contained_by': []
                }

            bags[bag_colour]['can_contain'][colour_name] = num
            if bag_colour not in bags[colour_name]['can_be_contained_by']:
                bags[colour_name]['can_be_contained_by'].append(bag_colour)

            pass


def part_1() -> Union[int, str]:
    global bags

    unchecked: set[str] = set(bags['shiny gold']['can_be_contained_by'])
    checked: set[str] = {"shiny gold"}

    while len(unchecked):
        bag_colour = unchecked.pop()

        if bag_colour in checked:
            continue

        for possible_new in bags[bag_colour]['can_be_contained_by']:
            if possible_new not in checked:
                unchecked.add(possible_new)

        checked.add(bag_colour)

    return len(checked) - 1


def part_2() -> Union[int, str]:
    global bags

    count = 0

    unchecked = ['shiny gold']

    while len(unchecked):
        bag_colour = unchecked.pop()

        for new in bags[bag_colour]['can_contain']:
            for _ in range(bags[bag_colour]['can_contain'][new]):
                unchecked.append(new)
                count += 1

    return count


if __name__ == "__main__":
    load_bags()
    print("Part 1:", part_1())
    print("\nPart 2:", part_2())
