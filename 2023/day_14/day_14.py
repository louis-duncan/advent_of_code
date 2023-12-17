from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2023/day/14
"""

def roll(grid: AgentCloud, direction: str):
    if direction == "N":
        point_list = grid.y_x_sorted
    elif direction == "E":
        point_list = grid.x_y_sorted[::-1]
    elif direction == "S":
        point_list = grid.y_x_sorted[::-1]
    else:
        point_list = grid.x_y_sorted

    for point in point_list:
        if point.value != "O":
            continue

        if direction == "N":
            next_points = grid.get_next_in_direction(point.x, point.y, "N")

            if len(next_points) == 0:
                new_y = 0
            else:
                new_y = next_points[-1].y + 1

            distance = point.y - new_y
        elif direction == "E":
            next_points = grid.get_next_in_direction(point.x, point.y, "E")

            if len(next_points) == 0:
                new_x = grid.max_x
            else:
                new_x = next_points[0].x - 1

            distance = new_x - point.x
        elif direction == "S":
            next_points = grid.get_next_in_direction(point.x, point.y, "S")

            if len(next_points) == 0:
                new_y = grid.max_y
            else:
                new_y = next_points[0].y - 1

            distance = new_y - point.y
        else:
            next_points = grid.get_next_in_direction(point.x, point.y, "W")

            if len(next_points) == 0:
                new_x = 0
            else:
                new_x = next_points[-1].x + 1

            distance = point.x - new_x

        if distance > 0:
            point.move(direction, distance)


def part_1() -> Union[int, str]:
    grid = AgentCloud(input_lines("input.txt"))

    roll(grid, "N")

    load = 0
    for point in grid.points:
        if point.value == "O":
            load += (grid.max_y - point.y) + 1

    return load


def part_2() -> Union[int, str]:
    grid = AgentCloud(input_lines("input.txt"))

    directions = "NWSE"
    states: dict[int, int] = {}  # state_hash: step
    i = 0
    caught_loop = False
    end = 1_000_000_000
    while i < end:
        for direction in directions:
            roll(grid, direction)
            #print()
            #print(direction)
            #print(grid)
        state = grid.state_hash
        if caught_loop:
            pass
        elif state in states:
            caught_loop = True
            i_last_seen = states[state]
            loop_len = i - i_last_seen
            iterations_left = end - i
            num_loops = iterations_left // loop_len
            i += num_loops * loop_len
        else:
            states[state] = i
        i += 1

        #print(i)
        #print(grid)

    load = 0
    for point in grid.points:
        if point.value == "O":
            load += (grid.max_y - point.y) + 1

    return load


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
