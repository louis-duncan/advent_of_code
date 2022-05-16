from __future__ import annotations

from typing import List

test_data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

data = """2344671212
6611742681
5575575573
3167848536
1353827311
4416463266
2624761615
1786561263
3622643215
4143284653"""


class Octo:
    def __init__(self, pos, energy_level):
        self.pos = pos
        self.energy_level = energy_level
        self.neighbours: List[Octo] = []
        self.flashing = False

    def add_neighbour(self, other: Octo):
        if other not in self.neighbours:
            self.neighbours.append(other)
        if self not in other.neighbours:
            other.neighbours.append(self)

    def increment_energy(self):
        self.energy_level += 1

    def resolve_flashing(self):
        if not self.flashing:
            if self.energy_level > 9:
                self.flashing = True
                for n in self.neighbours:
                    n.increment_energy()
                self.energy_level = 0

    def __repr__(self):
        return f"Octo(pos={self.pos}, energy_level={self.energy_level})"


def print_grid(grid: List[List[Octo]]):
    for row in grid:
        for octo in row:
            print(octo.energy_level, end="")
        print()


def main():
    global data
    grid = []
    all_octos = []
    for y, line in enumerate(data.split("\n")):
        new_row = [Octo([x, y], int(c)) for x, c in enumerate(line)]
        grid.append(new_row)
        for o in new_row:
            all_octos.append(o)

    for y in range(len(grid[0])):
        for x in range(len(grid)):
            if x > 0:
                grid[y][x].add_neighbour(grid[y][x-1])
                if y > 0:
                    grid[y][x].add_neighbour(grid[y-1][x-1])
                if y < len(grid) - 1:
                    grid[y][x].add_neighbour(grid[y+1][x-1])
            if x < len(grid[0]) - 1:
                grid[y][x].add_neighbour(grid[y][x+1])
                if y > 0:
                    grid[y][x].add_neighbour(grid[y-1][x+1])
                if y < len(grid) - 1:
                    grid[y][x].add_neighbour(grid[y+1][x+1])
            if y > 0:
                grid[y][x].add_neighbour(grid[y - 1][x])
            if y < len(grid) - 1:
                grid[y][x].add_neighbour(grid[y + 1][x])

    print_grid(grid)
    print()
    count = 0
    for step_num in range(300):
        step_count = 0
        for octo in all_octos:
            octo.increment_energy()

        while max([o.energy_level for o in all_octos]) > 9:
            for octo in all_octos:
                octo.resolve_flashing()

        for o in all_octos:
            if o.flashing:
                o.flashing = False
                o.energy_level = 0
                count += 1
                step_count += 1

        print_grid(grid)
        if step_count == len(all_octos):
            print(f"All Flashed! Step {step_num+1}")
            break
        print()
    print(f"Total Flashes: {count}")


if __name__ == '__main__':
    main()
