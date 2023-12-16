from functools import cached_property
from typing import Tuple, List, Union, Generator
from math import inf


class Line:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]):
        self.start = start
        self.end = end

    @cached_property
    def x_min(self) -> int:
        return min([self.start[0], self.end[0]])

    @cached_property
    def x_max(self) -> int:
        return max([self.start[0], self.end[0]])

    @cached_property
    def y_min(self) -> int:
        return min([self.start[1], self.end[1]])

    @cached_property
    def y_max(self) -> int:
        return max([self.start[1], self.end[1]])

    @property
    def coordinates(self) -> Generator[None, Tuple[int, int], None]:
        if self.x_min == self.x_max:
            for y in range(self.y_min, self.y_max + 1):
                yield self.start[0], y
        else:
            for x in range(self.x_min, self.x_max + 1):
                yield x, self.start[1]


class Grid:
    def __init__(self):
        self._grid = []
        self.x_min = inf
        self.x_max = 0
        self.y_min = inf
        self.y_max = 0

    def add(self, pos: Tuple[int, int], value: Union[str, None]):
        pass


def print_grid(grid: List[List[Union[str, None]]], highlight_pos=None):
    lines = []
    for y in range(len(grid[0])):
        line = ""
        for x in range(len(grid)):
            if highlight_pos is not None and highlight_pos[0] == x and highlight_pos[1] == y:
                line += "v"
            elif c := grid[x][y]:
                line += c
            else:
                line += " "

        lines.append(line)
    print("\n".join(lines))


def part_1():
    grid: List[List[Union[str, None]]] = []
    lines: List[Line] = []
    with open("input.txt", "r") as fh:
        _lines = [line.strip() for line in fh.readlines()]
        for _l in _lines:
            line_segs: List[str] = _l.split(" -> ")
            coords: List[Tuple[int, int]] = []
            for i in range(len(line_segs)):
                x_str, y_str = line_segs[i].split(",")
                coords.append((int(x_str), int(y_str)))
            for i in range(len(coords) - 1):
                lines.append(Line(coords[i], coords[i + 1]))

    x_min = min([line.x_min for line in lines])
    x_max = max([line.x_max for line in lines])
    y_min = min([line.y_min for line in lines] + [0])
    y_max = max([line.y_max for line in lines])
    y_max += 1
    x_offset = x_min
    y_offset = y_min

    for x in range(x_min, x_max + 1):
        grid.append([None for y in range(y_min, y_max + 1)])

    for line in lines:
        for x, y in line.coordinates:
            try:
                grid[x - x_offset][y - y_offset] = "█"
            except Exception as e:
                print(x, y)
                raise e

    #print_grid(grid)

    done = False
    input_pos = (500, 0)
    count = 0
    while not done:
        grain_done = False
        grain_pos = list(input_pos)
        while not grain_done:
            if grain_pos[0] == x_max:
                grid.append([None for y in range(len(grid[0]))])
                x_max += 1
            elif grain_pos[0] == x_min:
                grid.insert(0, [None for y in range(len(grid[0]))])
                x_min -= 1
                x_offset -= 1
            try:
                if grain_pos[1] == y_max:
                    grain_done = True
                elif grid[grain_pos[0] - x_offset][(grain_pos[1] + 1) - y_offset] is None:
                    grain_pos[1] += 1
                elif grid[(grain_pos[0] - 1) - x_offset][(grain_pos[1] + 1) - y_offset] is None:
                    grain_pos[1] += 1
                    grain_pos[0] -= 1
                elif grid[(grain_pos[0] + 1) - x_offset][(grain_pos[1] + 1) - y_offset] is None:
                    grain_pos[1] += 1
                    grain_pos[0] += 1
                else:
                    grain_done = True

                if grain_done:
                    grid[grain_pos[0] - x_offset][grain_pos[1] - y_offset] = "*"
                    count += 1
            except IndexError as e:
                grain_done = True
                done = True

            if grain_done and grain_pos[0] == input_pos[0] and grain_pos[1] == input_pos[1]:
                done = True
            #print()
            #print_grid(grid, [grain_pos[0] - x_offset, grain_pos[1] - y_offset])
            pass
    print_grid(grid)
    print(count)



if __name__ == '__main__':
    part_1()
