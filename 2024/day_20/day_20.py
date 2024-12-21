import time

import colour
import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/20
"""

_INPUT_PATH = INPUT_PATH  # _TEST


def part_1() -> Union[int, str]:
    grid = LineGrid(input_lines(_INPUT_PATH))
    start_pos = grid.find("S")
    end_pos = grid.find("E")
    
    path = grid.get_shortest_path(start_pos, end_pos, passable_values={"S", "E", "."})

    pretty(grid, path)


def part_2() -> Union[int, str]:
    ...


def pretty(grid: LineGrid, highlight_path: list[tuple[int, int]] = None):
    if highlight_path is None:
        highlight_path = []
    pretty_text = ""
    from PIL import Image
    image = Image.new(size=(grid.width, grid.height), mode="RGB")
    wall_options = {
        (True, True, True, True): "┼",
        (False, False, False, False): "▪",
        (True, False, False, False): "│",
        (False, True, False, False): "─",
        (False, False, True, False): "│",
        (False, False, False, True): "─",
        (True, False, True, False): "│",
        (False, True, False, True): "─",
        (True, True, False, False): "└",
        (False, True, True, False): "┌",
        (False, False, True, True): "┐",
        (True, False, False, True): "┘",
        (True, True, True, False): "├",
        (False, True, True, True): "┬",
        (True, False, True, True): "┤",
        (True, True, False, True): "┴",
    }
    colours = [
        colour.hsl2rgb(c) for c in colour.color_scale(
            colour.rgb2hsl((1, 0, 0)),
            colour.rgb2hsl((0, 0, 1)),
            len(highlight_path)
        )
    ]
    for y in range(grid.height):
        for x in range(grid.width):
            v = grid.get(x, y)
            if v == "S":
                image.putpixel((x, y), (0, 255, 0))
                pretty_text += "▒"
            elif v == "E":
                image.putpixel((x, y), (255, 0, 0))
                pretty_text += "▒"
            elif (x, y) in highlight_path:
                col = tuple([int(c * 255) for c in colours[highlight_path.index((x, y))]])
                image.putpixel((x, y), col)
                pretty_text += "*"
            elif v == "#":
                image.putpixel((x, y), (0, 0, 0))
                present_neighbours = []
                for nx, ny in [grid.get_neighbour_coord(x, y, d) for d in [0, 2, 4, 6]]:
                    if grid.is_pos_in_bounds(nx, ny):
                        present_neighbours.append(grid.get(nx, ny) == "#")
                    else:
                        present_neighbours.append(False)
                pretty_text += wall_options[tuple(present_neighbours)]
            else:
                image.putpixel((x, y), (255, 255, 255))
                pretty_text += " "
        pretty_text += "\n"

    with open("pretty_input.txt", "w", encoding="utf-8") as fh:
        fh.write(pretty_text)

    image.save("pretty_input.png")


if __name__ == "__main__":
    p1_start = time.time()
    part_1_answer = part_1()
    p1_duration = time.time() - p1_start
    if part_1_answer is not None:
        print(f"Part 1 ({p1_duration * 1000:.2f}ms):", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    p2_start = time.time()
    part_2_answer = part_2()
    p2_duration = time.time() - p2_start
    if part_2_answer is not None:
        print(f"Part 2 ({p2_duration * 1000:.2f}ms):", part_2_answer)
        pyperclip.copy(part_2_answer)
