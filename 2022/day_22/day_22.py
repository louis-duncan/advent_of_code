import re
from math import inf
from typing import List, Tuple, Dict


class Map:
    def __init__(self, map_str: str):
        self.player_direction = 0

        self.places: Dict[Tuple[int, int], int] = {}

        map_str_lines = map_str.split("\n")

        max_x = 0
        max_y = len(map_str_lines)

        for yish, line in enumerate(map_str_lines):
            y = yish + 1
            for xish, c in enumerate(line):
                x = xish + 1
                if x > max_x:
                    max_x = x
                if c != " ":
                    self.places[(x, y)] = int(c == "#")

        self.row_limits = []
        self.column_limits = []

        for y in range(1, max_y + 1):
            start_x = 0
            end_x = max_x
            in_bounds = False
            for x in range(1, max_x + 1):
                cell = self.places.get((x, y))
                if not in_bounds and cell is not None:
                    in_bounds = True
                    start_x = x
                elif in_bounds and cell is None:
                    end_x = x - 1
                    break
            self.row_limits.append((start_x, end_x))

        for x in range(1, max_x + 1):
            start_y = 0
            end_y = max_y
            in_bounds = False
            for y in range(1, max_y + 1):
                cell = self.places.get((x, y))
                if not in_bounds and cell is not None:
                    in_bounds = True
                    start_y = y
                elif in_bounds and cell is None:
                    end_y = y - 1
                    break
            self.column_limits.append((start_y, end_y))

        self.player_pos = (self.row_limits[0][0], 1)

    def turn(self, direction: int):
        self.player_direction = (self.player_direction + direction) % 4

    def move(self, distance):
        for _ in range(distance):
            next_pos = self.next_pos()
            if self.places[next_pos] == 0:
                self.player_pos = next_pos
            else:
                break

    def next_pos(self):
        x, y = self.player_pos

        if self.player_direction == 3:
            y -= 1
            if y < self.column_limits[x - 1][0]:
                y = self.column_limits[x - 1][1]
        elif self.player_direction == 0:
            x += 1
            if x > self.row_limits[y - 1][1]:
                x = self.row_limits[y - 1][0]
        elif self.player_direction == 1:
            y += 1
            if y > self.column_limits[x - 1][1]:
                y = self.column_limits[x - 1][0]
        elif self.player_direction == 2:
            x -= 1
            if x < self.row_limits[y - 1][0]:
                x = self.row_limits[y - 1][1]
        else:
            raise ValueError(f"Invalid direction {self.player_direction}")
        return x, y


def load_map():
    with open("input.txt", "r") as fh:
        map_str, instruction_str = fh.read().split("\n\n")
        space = Map(map_str)
    instructions = re.findall(r"([0-9]+|L|R)", instruction_str)
    for i in range(len(instructions)):
        try:
            instructions[i] = int(instructions[i])
        except ValueError:
            pass
    return space, instructions


def main():
    space, instructions = load_map()

    try:
        for inst in instructions:
            if inst == "L":
                space.turn(-1)
            elif inst == "R":
                space.turn(1)
            else:
                space.move(inst)
    except Exception as e:
        print(f"Exception {e.__class__.__name__}({e})")

    return space


if __name__ == '__main__':
    state = main()
    print((state.player_pos[1] * 1000) + (state.player_pos[0]  * 4) + state.player_direction)

