import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/21
"""

_INPUT_PATH = INPUT_PATH_TEST

KEYPAD_MAP = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3)
}

DIRECTION_PAD_MAP = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1)
}

robot_positions: list[tuple[int, int]] = [(2, 3), (0, 2), (0, 2), (0, 2)]


def buttons_to_coords_keypad(target_buttons: str) -> list[tuple[int, int]]:
    return [KEYPAD_MAP[t] for t in target_buttons]


def buttons_to_coords_direction_pad(target_buttons: str) -> list[tuple[int, int]]:
    return [DIRECTION_PAD_MAP[t] for t in target_buttons]


def get_needed_moves(start: tuple[int, int], end: tuple[int, int]) -> dict[str, int]:
    m = {
        '^': 0,
        '>': 0,
        'v': 0,
        '<': 0,
    }
    dx = abs(end[0] - start[0])
    if end[0] > start[0]:
        m['>'] += dx
    else:
        m['<'] += dx
    dy = abs(end[1] - start[1])
    if end[1] > start[1]:
        m['v'] += dy
    else:
        m['^'] += dy
    return m


def moves_keypad(origin: tuple[int, int], target_coords: list[tuple[int, int]]) -> str:
    moves: str = ""
    current_pos = origin
    for t in target_coords:
        needed_moves = get_needed_moves(current_pos, t)

        while max(needed_moves.values()):
            if needed_moves['<'] and not (current_pos[1] == 3 and current_pos[0] - needed_moves['<'] == 0):
                moves += needed_moves['<'] * "<"
                current_pos = (current_pos[0] - needed_moves['<'], current_pos[1])
                needed_moves['<'] = 0
            elif needed_moves['v'] and not (current_pos[0] == 0 and current_pos[1] + needed_moves['v'] == 3):
                moves += needed_moves['v'] * "v"
                current_pos = (current_pos[0], current_pos[1] + needed_moves['v'])
                needed_moves['v'] = 0
            elif needed_moves['^']:
                moves += "^" * needed_moves['^']
                current_pos = (current_pos[0], current_pos[1] - needed_moves['^'])
                needed_moves['^'] = 0
            elif needed_moves['>']:
                moves += ">" * needed_moves['>']
                current_pos = (current_pos[0] + needed_moves['>'], current_pos[1])
                needed_moves['>'] = 0

        moves += "A"
        current_pos = t

    return moves


def moves_direction_pad(origin: tuple[int, int], target_coords: list[tuple[int, int]]) -> str:
    moves: str = ""
    current_pos = origin
    for t in target_coords:
        needed_moves = get_needed_moves(current_pos, t)

        while max(needed_moves.values()):
            if needed_moves['<'] and not (current_pos[1] == 0 and current_pos[0] - needed_moves['<'] == 0):
                moves += needed_moves['<'] * "<"
                current_pos = (current_pos[0] - needed_moves['<'], current_pos[1])
                needed_moves['<'] = 0
            elif needed_moves['v'] and not (current_pos[0] == 0 and current_pos[1] - needed_moves['v'] == 0):
                moves += needed_moves['v'] * "v"
                current_pos = (current_pos[0], current_pos[1] + needed_moves['v'])
                needed_moves['v'] = 0
            elif needed_moves['^']:
                moves += "^" * needed_moves['^']
                current_pos = (current_pos[0], current_pos[1] - needed_moves['^'])
                needed_moves['^'] = 0
            elif needed_moves['>']:
                moves += ">" * needed_moves['>']
                current_pos = (current_pos[0] + needed_moves['>'], current_pos[1])
                needed_moves['>'] = 0

        moves += "A"
        current_pos = t

    return moves


def part_1() -> Union[int, str]:
    result = 0

    for line in input_lines(_INPUT_PATH):
        line = line.strip()

        keypad_coords = buttons_to_coords_keypad(line)
        new_moves = moves_keypad(
            origin=robot_positions[0],
            target_coords=keypad_coords
        )
        robot_positions[0] = keypad_coords[-1]
        print(new_moves)

        dir_pad_coords = buttons_to_coords_direction_pad(new_moves)
        new_moves = moves_direction_pad(
            origin=robot_positions[1],
            target_coords=dir_pad_coords
        )
        robot_positions[1] = dir_pad_coords[-1]
        print(new_moves)

        dir_pad_coords = buttons_to_coords_direction_pad(new_moves)
        new_moves = moves_direction_pad(
            origin=robot_positions[2],
            target_coords=dir_pad_coords
        )
        robot_positions[2] = dir_pad_coords[-1]

        dir_pad_coords = buttons_to_coords_direction_pad(new_moves)
        new_moves = moves_direction_pad(
            origin=robot_positions[3],
            target_coords=dir_pad_coords
        )
        robot_positions[3] = dir_pad_coords[-1]

        print(new_moves)
        result += len(new_moves) * int(re.findall(r"\d+", line)[0])
        break



    return result



def part_2() -> Union[int, str]:
    ...


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
