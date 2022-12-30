import collections
import hashlib
from typing import List, Generator, Union, Tuple, Iterator
from copy import deepcopy


class Direction:
    LEFT = 0
    RIGHT = 1
    DOWN = 2


class JumpableRange:
    def __init__(self, n: int):
        self.cur = -1
        self.end = n

    def __next__(self):
        self.cur += 1
        if self.cur >= self.end:
            raise StopIteration
        return self.cur

    def skip_to(self, n):
        self.cur = n


class JumpableListIter:
    def __iter__(self):
        return self

    def __init__(self, obj):
        self.list = obj
        self.list_len = len(self.list)
        self.next_index = 0

    def __next__(self):
        v = self.list[self.next_index]

        self.next_index += 1
        self.next_index %= self.list_len

        return v

    def skip_to(self, n):
        self.next_index = n % self.list_len


shape_shapes = {
    '-': [
        [1, 1, 1, 1]
    ],
    '+': [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ],
    'J': [
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    'I': [
        [1],
        [1],
        [1],
        [1],
    ],
    'X': [
        [1, 1],
        [1, 1]
    ]
}


def can_shape_move(shape: str, pos: Tuple[int, int], grid: List[List[int]], direction: int) -> bool:
    shape_grid: List[List[int]] = shape_shapes[shape]

    match direction:
        case Direction.RIGHT:
            pos = (pos[0] + 1, pos[1])
        case Direction.LEFT:
            pos = (pos[0] - 1, pos[1])
        case Direction.DOWN:
            pos = (pos[0], pos[1] + 1)
        case _:
            pass

    if pos[0] < 0:
        return False
    elif pos[0] + len(shape_grid[0]) > len(grid[0]):
        return False
    elif pos[1] + len(shape_grid) > len(grid):
        return False

    for ys in range(len(shape_grid)):
        for xs in range(len(shape_grid[0])):
            xg = xs + pos[0]
            yg = ys + pos[1]

            if shape_grid[ys][xs] + grid[yg][xg] == 2:
                return False

    return True


def move_if_possible(shape: str, pos: Tuple[int, int], grid: List[List[int]], direction: int) -> Tuple[int, int]:
    if can_shape_move(shape, pos, grid, direction):
        if direction == Direction.LEFT:
            return pos[0] - 1, pos[1]
        elif direction == Direction.RIGHT:
            return pos[0] + 1, pos[1]
        elif direction == Direction.DOWN:
            return pos[0], pos[1] + 1
    else:
        return pos


def commit_shape(shape: str, pos: Tuple[int, int], grid: List[List[int]]):
    shape_grid: List[List[int]] = shape_shapes[shape]
    for ys in range(len(shape_grid)):
        for xs in range(len(shape_grid[0])):
            xg = xs + pos[0]
            yg = ys + pos[1]
            grid[yg][xg] += shape_grid[ys][xs]


def trim_grid(grid: List[List[int]]) -> int:
    """
    hits = 0
    target = (2 ** len(grid[0])) - 1

    y = 0
    for y in range(len(grid)):
        hits |= sum([grid[y][x] << x for x in range(len(grid[0]))])
        if hits == target:
            break

    start_len = len(grid)
    num_to_trim = start_len - (y + 1)
    """
    num_to_trim = max(0, len(grid) - (first_occupied_y(grid) + 100))
    for i in range(num_to_trim):
        grid.pop(-1)

    return num_to_trim


def first_occupied_y(grid: List[List[int]]) -> int:
    y = 0
    for y in range(len(grid)):
        if 1 in grid[y]:
            return y
    else:
        return y + 1


def pad_grid(grid: List[List[int]]):
    num_to_insert = max(0, (4 + 3) - first_occupied_y(grid))
    for _ in range(num_to_insert):
        grid.insert(0, [0 for _ in range(len(grid[0]))])


def get_shape_start_pos(shape: str, grid: List[List[int]]) -> Tuple[int, int]:
    top_y = first_occupied_y(grid)
    shape_height = len(shape_shapes[shape])
    return 2, ((top_y - 4) - shape_height) + 1


def list_cycle(subject_list: List[Union[int, str]]) -> Generator[Tuple[int, Union[int, str]], None, None]:
    i = 0
    len_list = len(subject_list)
    while True:
        yield i, subject_list[i]
        i += 1
        i %= len_list


def hash_state(grid, last_shape_n, last_effect_n) -> int:
    hasher = hashlib.sha256()

    hasher.update(
        last_shape_n.to_bytes(
            (last_shape_n // 254) + (last_shape_n % 254 != 0),
            "big"
        )
    )
    hasher.update(
        last_effect_n.to_bytes(
            (last_effect_n // 254) + (last_effect_n % 254 != 0),
            "big"
        )
    )

    started = False
    for row in grid:
        if 1 in row:
            started = True

        if started:
            row_value = sum([row[x] << x for x in range(len(row))])
            hasher.update(
                row_value.to_bytes(
                    (row_value // 254) + (row_value % 254 != 0),
                    "big"
                )
            )

    return int.from_bytes(hasher.digest(), "big")


def main():
    with open("input.txt", "r") as fh:
        effects_list = [Direction.LEFT if c == "<" else Direction.RIGHT for c in fh.read().strip()]

    effect_feed = JumpableListIter(effects_list)
    shape_feed = JumpableListIter(list(shape_shapes.keys()))

    num_rocks = 1000000000000

    grid = [
        [0, 0, 0, 0, 0, 0, 0]
    ]
    num_trimmed_lines = 0
    seen_states = {}
    rock_count = 0

    #print_grid(grid)

    en = 0
    while rock_count < num_rocks:
        sn = shape_feed.next_index
        shape = next(shape_feed)
        pad_grid(grid)
        pos = get_shape_start_pos(shape, grid)
        for direction in effect_feed:
            en = effect_feed.next_index - 1
            pos = move_if_possible(shape, pos, grid, direction)

            can_move = can_shape_move(shape, pos, grid, Direction.DOWN)
            if can_move:
                pos = (pos[0], pos[1] + 1)
            else:
                commit_shape(shape, pos, grid)
                break

        rock_count += 1

        trimmed = trim_grid(grid)

        num_trimmed_lines += trimmed

        current_height = (len(grid) - first_occupied_y(grid)) + num_trimmed_lines
        state_hash = hash_state(grid, sn, en)
        if state_hash not in seen_states:
            seen_states[state_hash] = (rock_count, current_height)
        else:
            shapes_diff = rock_count - seen_states[state_hash][0]
            height_diff = current_height - seen_states[state_hash][1]
            remaining_rocks = num_rocks - rock_count

            repeats_to_add = remaining_rocks // shapes_diff

            shapes_to_add = repeats_to_add * shapes_diff
            height_to_add = repeats_to_add * height_diff

            print(f"added {repeats_to_add} instances of {shapes_to_add} shapes and {height_to_add} height.")

            shape_feed.skip_to(shape_feed.next_index + shapes_to_add)
            rock_count += shapes_to_add
            num_trimmed_lines += height_to_add

    print((len(grid) - first_occupied_y(grid)) + num_trimmed_lines)


def print_grid(grid: List[List[int]], shape=None, shape_pos=None):
    t_grid = deepcopy(grid)
    if None not in (shape, shape_pos):
        commit_shape(shape, shape_pos, t_grid)

    for row in t_grid:
        print("".join(str(n) for n in row))

    print()


if __name__ == '__main__':
    main()

    """_grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    #print_grid(_grid)
    print(can_shape_move("-", (2, 6), _grid, Direction.DOWN))"""

