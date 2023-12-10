from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2023/day/10
"""


class PipeGrid(LineGrid):
    out_directions = {
        "S": set("NESW"),
        "|": set("NS"),
        "-": set("EW"),
        "L": set("NE"),
        "J": set("NW"),
        "7": set("SW"),
        "F": set("ES"),
        ".": set()
    }
    in_directions = {
        "S": set("NESW"),
        "|": set("NS"),
        "-": set("EW"),
        "L": set("WS"),
        "J": set("ES"),
        "7": set("NE"),
        "F": set("NW"),
        ".": set()
    }

    def find_connections(self, x: int, y: int) -> list[tuple[int, int]]:
        """Find all connections to given position"""
        current_location_value = self.get(x, y)
        # Determine directions connections could be based on current location
        directions_to_check = self.out_directions[current_location_value]
        connections: list[tuple[int, int]] = []
        for direction in directions_to_check:
            try:
                neighbour, n_x, n_y = self.get_neighbour(x, y, direction)
                if direction not in self.in_directions[neighbour]:
                    raise ValueError(f"Tried to go {direction} into {neighbour} at {n_x}, {n_y}")
                connections.append((n_x, n_y))
            except ValueError:
                pass
        return connections


def find_loop(grid: PipeGrid) -> list[tuple[int, int]]:
    start_pos = grid.find("S")
    loop: list[tuple[int, int]] = [start_pos, grid.find_connections(*start_pos)[0]]
    looped = False
    while not looped:
        possible_new = grid.find_connections(*loop[-1])
        assert len(possible_new) == 2

        if start_pos in possible_new and loop[-2] != start_pos:
            looped = True
            continue

        if possible_new[0] != loop[-2]:
            loop.append(possible_new[0])
        else:
            loop.append(possible_new[1])
    return loop


def part_1() -> Union[int, str]:
    grid = PipeGrid(input_lines("input.txt"))
    loop = find_loop(grid)
    return len(loop) // 2


def part_2() -> Union[int, str]:
    grid = PipeGrid(input_lines("input.txt"))
    loop = find_loop(grid)
    loop_set = set(loop)

    start_neighbour_directions = {
        grid.get_direction(*loop[0], *loop[1]),
        grid.get_direction(*loop[0], *loop[-1])
    }
    for symbol, directions in grid.out_directions.items():
        if directions == start_neighbour_directions:
            grid.set(loop[0][0], loop[0][1], symbol)
            break

    count = 0
    for x in range(grid.width):
        entry_loop_char = ""
        inside = False
        for y in range(grid.height):
            current_pos = (x, y)
            current = grid.get(x, y)
            if (x, y) in loop_set:
                if current == "-":
                    inside = not inside
                elif not entry_loop_char:
                    entry_loop_char = current
                else:
                    if entry_loop_char == "F" and current == "L":
                        entry_loop_char = ""
                    elif entry_loop_char == "F" and current == "J":
                        inside = not inside
                        entry_loop_char = ""
                    elif entry_loop_char == "7" and current == "J":
                        entry_loop_char = ""
                    elif entry_loop_char == "7" and current == "L":
                        inside = not inside
                        entry_loop_char = ""
            else:
                entry_loop_char = ""
                count += inside
    return count


if __name__ == "__main__":
    part_1_answer = part_1()
    if part_1_answer is not None:
        print("Part 1:", part_1())
        pyperclip.copy(part_1_answer)

    part_2_answer = part_2()
    if part_2_answer is not None:
        print()
        print("Part 2:", part_2())
        pyperclip.copy(part_2_answer)
