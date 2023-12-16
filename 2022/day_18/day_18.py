import hashlib
import re
from math import inf
from typing import Tuple, List, Set
from collections import deque


class Cube:
    def __init__(self, pos: Tuple[int, int, int]):
        self.x, self.y, self.z = pos
        self.links: List[Cube] = []
        self.num_links: int = 0
        self.num_ext_faces: int = 6
        self.at_limit = False
        self.visited = False

    def __repr__(self):
        return f"Cube(pos={self.pos})"

    @property
    def pos(self) -> Tuple[int, int, int]:
        return self.x, self.y, self.z

    def link(self, other: 'Cube'):
        self.links.append(other)
        self.num_links += 1
        self.num_ext_faces -= 1
        other.links.append(self)
        other.num_links += 1
        other.num_ext_faces -= 1

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other: 'Cube'):
        return self.pos == other.pos


class CubeSet(set):
    def __init__(self):
        super().__init__()

        # noinspection PyTypeChecker
        self.min_pos: List[int] = [inf, inf, inf]
        # noinspection PyTypeChecker
        self.max_pos: List[int] = [-inf, -inf, -inf]

        self.cube_hashes: Set[int] = set()

    def add(self, new: Cube):
        super().add(new)
        self.cube_hashes.add(hash(new))

        for i, n in enumerate(new.pos):
            if n < self.min_pos[i]:
                self.min_pos[i] = n
            if n > self.max_pos[i]:
                self.max_pos[i] = n

    def generate_links(self):
        for cube_1 in self:
            for cube_2 in self:
                if cube_1 is cube_2:
                    continue
                if manhattan_distance(cube_1.pos, cube_2.pos) == 1 and cube_2 not in cube_1.links:
                    cube_1.link(cube_2)

    def contains_cube(self, other: Cube) -> bool:
        return hash(other) in self.cube_hashes


def manhattan_distance(pos_1: Tuple[int, int, int], pos_2: Tuple[int, int, int]) -> int:
    return abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1]) + abs(pos_1[2] - pos_2[2])


def sum_linked_cubes_faces(root: Cube) -> int:
    tagged: List[Cube] = []
    to_count = deque()
    to_count.append(root)
    tot = 0

    while len(to_count) > 0:
        cur_cube = to_count.pop()
        if cur_cube.visited:
            continue
        cur_cube.visited = True
        tagged.append(cur_cube)

        if not cur_cube.at_limit:
            tot += cur_cube.num_ext_faces

        for c in cur_cube.links:
            if not c.visited:
                to_count.append(c)

    print("traversed", len(tagged))

    for t in tagged:
        t.visited = False

    return tot


def main():
    internal_set: CubeSet[Cube] = CubeSet()

    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            match = re.findall(r"(\d*),(\d*),(\d*)", line.strip())
            new_pos = (int(match[0][0]), int(match[0][1]), int(match[0][2]))
            internal_set.add(Cube(new_pos))
    internal_set.generate_links()

    print("generated internal")

    # Generate inverted set
    inverted_set: CubeSet[Cube] = CubeSet()
    min_x, max_x = internal_set.min_pos[0] - 2, internal_set.max_pos[0] + 2
    min_y, max_y = internal_set.min_pos[1] - 2, internal_set.max_pos[1] + 2
    min_z, max_z = internal_set.min_pos[2] - 2, internal_set.max_pos[2] + 2

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                new = Cube((x, y, z))
                if x == min_x or x == max_x or y == min_y or y == max_y or z == min_z or z == max_z:
                    new.at_limit = True
                if not internal_set.contains_cube(new):
                    inverted_set.add(new)
    inverted_set.generate_links()

    print("generated inverted")

    root = None
    for c in inverted_set:
        if c.pos == (min_x, min_y, min_z):
            root = c
            break
    assert root is not None

    print("found root, counting...")

    print(sum([c.num_ext_faces for c in internal_set]))
    print(sum_linked_cubes_faces(next(iter(inverted_set))))


if __name__ == '__main__':
    main()
