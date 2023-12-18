from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2023/day/16
"""


class Optic:
    grid = BasicGrid(0, 0)

    def __init__(self, x: int, y: int, symbol: str):
        self.x = x
        self.y = y
        self.grid.set(self, x, y)

        self.symbol = symbol
        self.activated_in = [False, False, False, False]
        self.activated_out = [False, False, False, False]

    def __repr__(self) -> str:
        return f"Optic(symbol='{self.symbol}'', x={self.x}, y={self.y})"

    def activate(self, direction_from: int) -> list['Optic']:
        direction = check_direction(direction_from)

        if self.activated_in[direction]:
            return []

        output_before = self.activated_out.copy()

        self.activated_in[direction_from] = True

        # Update outputs
        if self.symbol == "-":
            if direction == 0 or direction == 2:
                self.activated_out[1] = self.activated_out[3] = True
            elif direction == 1:
                self.activated_out[3] = True
            else:
                self.activated_out[1] = True
        elif self.symbol == "|":
            if direction == 1 or direction == 3:
                self.activated_out[0] = self.activated_out[2] = True
            elif direction == 0:
                self.activated_out[2] = True
            else:
                self.activated_out[0] = True
        elif self.symbol == "/":
            if direction == "0":
                self.activated_out[3] = True
            elif direction == "1":
                self.activated_out[2] = True
            elif direction == "2":
                self.activated_out[1] = True
            else:
                self.activated_out[0] = True
        elif self.symbol == "\\":
            if direction == "0":
                self.activated_out[1] = True
            elif direction == "1":
                self.activated_out[0] = True
            elif direction == "2":
                self.activated_out[3] = True
            else:
                self.activated_out[2] = True
        else:
            out_d = (direction + 2) % 4
            self.activated_out[out_d] = True

        # Check outputs against pre and return new activated neighbours
        result: list['Optic'] = []
        for i in range(4):
            if self.activated_out[i] and not output_before[i]:
                n = self.get_neighbour(i)
                if n is not None:
                    result.append(n)
        return result

    def get_neighbour(self, direction: int) -> 'Optic':
        if direction == 0:
            return self.grid.get(self.x, self.y - 1)
        elif direction == 1:
            return self.grid.get(self.x + 1, self.y)
        elif direction == 2:
            return self.grid.get(self.x, self.y + 1)
        else:
            return self.grid.get(self.x - 1, self.y)


def part_1() -> Union[int, str]:
    line_grid = LineGrid(input_lines("test_input.txt"))
    Optic.grid = BasicGrid(width=line_grid.width, height=line_grid.height)

    for y in range(line_grid.height):
        for x in range(line_grid.width):
            _ = Optic(x, y, line_grid.get(x, y))

    pass




def part_2() -> Union[int, str]:
    ...


if __name__ == "__main__":
    part_1_answer = part_1()
    if part_1_answer is not None:
        print("Part 1:", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    part_2_answer = part_2()
    if part_2_answer is not None:
        print("Part 2:", part_2_answer)
        pyperclip.copy(part_2_answer)
