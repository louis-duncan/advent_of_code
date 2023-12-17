from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2023/day/11
"""


class GalaxyGrid(LineGrid):
    def __init__(self, lines: Iterator[str]):
        super().__init__(lines)

    def expand(self, scale=2):
        y = 0
        while y < self.height:
            row = self.get_row(y)
            if min(row) == max(row) == ".":
                for _ in range(scale - 1):
                    self.insert_row(y, ".")
                y += scale - 1
            y += 1
        x = 0
        while x < self.width:
            col = self.get_col(x)
            if min(col) == max(col) == ".":
                for _ in range(scale - 1):
                    self.insert_col(x, ".")
                x += scale - 1
            x += 1


def tests():
    galax_grid = GalaxyGrid(input_lines("input.txt"))
    galaxies_pre = set(galax_grid.find_all("#"))
    galax_grid.expand(2)
    galaxies_post = set(galax_grid.find_all("#"))

    point_cloud = PointCloud(input_lines("input.txt"))
    point_pre = set([p.x_y for p in point_cloud.points])
    point_cloud.expand_11_23(2)
    points_post = set([p.x_y for p in point_cloud.points])

    p_diff = points_post.difference(galaxies_post)
    g_diff = galaxies_post.difference(points_post)
    x_max = max(max([p.x for p in point_cloud.points]), max([p[0] for p in galaxies_post]))
    y_max = max(max([p.y for p in point_cloud.points]), max([p[1] for p in galaxies_post]))
    g = LineGrid(["." * (x_max + 1) for _ in range(y_max + 1)])
    for p in p_diff:
        g.set(p[0], p[1], "#")
    for p in g_diff:
        g.set(p[0], p[1], "?")
    with open("test_out.txt", "w") as fh:
        fh.write(str(g))


    pass


def part_1() -> Union[int, str]:
    grid = GalaxyGrid(input_lines("input.txt"))
    grid.expand(2)
    galaxies = grid.find_all("#")
    total = 0
    for i in range(len(galaxies)):
        for j in range(i, len(galaxies)):
            total += manhattan_distance(
                galaxies[i],
                galaxies[j]
            )
    return total


def part_2() -> Union[int, str]:
    grid = PointCloud(input_lines("input.txt"))
    grid.expand_11_23(1_000_000)
    total = 0
    for i in range(len(grid.points)):
        for j in range(i, len(grid.points)):
            total += manhattan_distance(
                grid.points[i],
                grid.points[j]
            )
    return total


if __name__ == "__main__":
    #tests()

    part_1_answer = part_1()
    if part_1_answer is not None:
        print("Part 1:", part_1())
        pyperclip.copy(part_1_answer)

    part_2_answer = part_2()
    if part_2_answer is not None:
        print()
        print("Part 2:", part_2())
        pyperclip.copy(part_2_answer)
