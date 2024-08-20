import bisect
import logging
from math import inf
from pathlib import Path
from typing import Union, Optional, Type, Iterator, Any, Generator, Iterable, Callable

INPUT_PATH = "input.txt"
TEST_INPUT_PATH = "test_input.txt"
VALID_DIRECTIONS = ["N", "E", "S", "W", "U", "R", "D", "L", "0", "1", "2", "3", 0, 1, 2, 3]


def raw_input(input_path: Union[Path, str] = Path("test_input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read()
    return data


def input_lines(
        input_path: Union[Path, str] = Path("test_input.txt"),
        convert_type: Optional[Type] = None
) -> Generator[str, None, None]:
    for line in raw_input(input_path).strip().split("\n"):
        if convert_type is None:
            yield line.strip()
        else:
            yield convert_type(line.strip())


def grouped_input_lines(
        input_path: Union[Path, str] = Path("test_input.txt"),
        convert_type: Optional[Type] = None
) -> Generator[list[str], None, None]:
    """Return groups of lines from files with \n separators"""
    group: list[str] = []
    for line in input_lines(input_path, convert_type):
        if line == "":
            yield group
            group = []
        else:
            group.append(line)
    if group:
        yield group


class BasicGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.rows: list[list] = [[None for _ in range(width)] for _ in range(height)]

    def get(self, x: int, y: int) -> Any:
        if x < 0 or y < 0:
            return None
        try:
            return self.rows[y][x]
        except IndexError:
            return None

    def set(self, value, x: int, y: int) -> None:
        self.rows[y][x] = value

    def items(self) -> Generator[Any, None, None]:
        for y in range(self.width):
            for x in range(self.height):
                yield self.rows[y][x]


class LineGrid:
    def __init__(self, lines: Iterable[str], pad: str = "."):
        self.lines: list[list[str]] = [list(line.strip("\n\r")) for line in lines]
        if self.lines[-1] == "":
            self.lines.pop(-1)
        self.pad = pad

        line_lengths = [len(line) for line in self.lines]
        if min(line_lengths) != max(line_lengths):
            logging.warning(f"Grid has lines of different lengths. Lines will be padded with '{self.pad}'s")
            max_len = max(line_lengths)
            for i in range(len(self.lines)):
                for _ in range(max_len - len(self.lines[i])):
                    self.lines[i].append(self.pad)

        self.width: int = len(self.lines[0])
        self.height: int = len(self.lines)

    def _pos_in_bounds(self, x: int, y: int):
        if x < 0 or x >= self.width:
            return False
        elif y < 0 or y >= self.height:
            return False
        else:
            return True

    def _pos_check(self, x: int, y: int, wrap: int) -> [int, int]:
        in_bounds = self._pos_in_bounds(x, y)
        if not in_bounds and not wrap:
            raise ValueError(f"Position {x}, {y} is out of bounds")
        elif not in_bounds and wrap:
            x = x % self.width
            y = y % self.height
        return x, y

    def get(self, x: int, y: int, wrap=False) -> Union[str, int]:
        self._pos_check(x, y, wrap)
        return self.lines[y][x]

    def get_row(self, row_index: int) -> list[str]:
        return self.lines[row_index]

    @property
    def rows(self) -> Generator[list[str], None, None]:
        for i in range(self.height):
            yield self.get_row(i)

    def get_col(self, col_index: int) -> list[str]:
        return [line[col_index] for line in self.lines]

    @property
    def columns(self) -> Generator[list[str], None, None]:
        for i in range(self.width):
            yield self.get_col(i)

    def insert_row(self, index: int, fill="."):
        self.lines.insert(index, [fill for _ in range(self.width)])
        assert len(self.lines) == self.height + 1
        self.height += 1

    def insert_col(self, index: int, fill="."):
        for line in self.lines:
            line.insert(index, fill)
        assert len(self.lines[0]) == self.width + 1
        self.width += 1

    @classmethod
    def get_direction(cls, x1, y1, x2, y2) -> str:
        """Gives a NESW direction of 2 from 1"""
        direction = ""
        if y2 < y1:
            direction += "N"
        elif y2 > y1:
            direction += "S"
        if x2 < x1:
            direction += "W"
        elif x2 > x1:
            direction += "E"
        return direction

    def __quick_get(self, x: int, y: int) -> Union[str, int]:
        return self.lines[y][x]

    def set(self, x: int, y: int, value: Union[str, int], wrap=False):
        self._pos_check(x, y, wrap)
        self.lines[y][x] = value

    def find(self, value: Any, start_x: int = 0, start_y: int = 0) -> tuple[int, int]:
        """Returns first instance of value"""
        for y in range(start_y, self.height):
            for x in range(start_x, self.width):
                if self.__quick_get(x, y) == value:
                    return x, y
        else:
            raise ValueError(f"{value} is not in grid")

    def find_all(self, value: Any, start_x: int = 0, start_y: int = 0) -> list[tuple[int, int]]:
        """Returns coords for all instances of value"""
        found: list[tuple[int, int]] = []
        for y in range(start_y, self.height):
            for x in range(start_x, self.width):
                if self.__quick_get(x, y) == value:
                    found.append((x, y))
        return found

    def find_all_not(self, value: Any, start_x: int = 0, start_y: int = 0) -> list[tuple[int, int]]:
        """Returns coords of all instances of values != to the given value"""
        found: list[tuple[int, int]] = []
        for y in range(start_y, self.height):
            for x in range(start_x, self.width):
                if self.__quick_get(x, y) != value:
                    found.append((x, y))
        return found

    @classmethod
    def get_neighbor_coord(cls, x: int, y: int, direction: Union[int, str]) -> tuple[int, int]:
        direction = check_direction(direction)
        if direction == 0:
            y -= 1
        elif direction == 1:
            x += 1
        elif direction == 2:
            y += 1
        else:
            x -= 1
        return x, y

    def get_neighbour(
            self,
            x: int,
            y: int,
            direction: Union[str, int],
            wrap=False) -> tuple[Union[str, int], int, int]:
        """
        Directions: any 1 or 2 char combination of N, W, S, W or U, D, L, R
        returns: neighbour value, x, y
        """
        direction = check_direction(direction)
        x, y = self.get_neighbor_coord(x, y, direction)
        return self.get(x, y, wrap), x, y

    def flood_fill(self, value: str, x: int, y: int) -> int:
        to_fill = self.get(x, y)
        count = 0
        queue: list[tuple[int, int]] = [(x, y), ]

        while len(queue):
            current = queue.pop(0)
            try:
                if self.get(current[0], current[1]) == to_fill:
                    count += 1
                    self.set(current[0], current[1], value)
                    for d in range(0, 4):
                        queue.append(self.get_neighbor_coord(current[0], current[1], d))
            except ValueError:
                pass

        return count

    def __str__(self):
        return "\n".join(["".join(line) for line in self.lines])

    def iterate_x_y(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x, y


class Point:
    def __init__(self, value: Union[str, int], x: int, y: int):
        self.value = value
        self.x = x
        self.y = y
        self.cloud: Optional['PointGrid'] = None

    @property
    def x_y(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def y_x(self) -> tuple[int, int]:
        return self.y, self.x

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={repr(self.value)}, x={self.x}, y={self.y})"

    def get_neighbours(self, direction: Union[int, str]) -> list['Point']:
        if self.cloud is None:
            raise ValueError("Point does not have a cloud")

        direction = check_direction(direction)

        n_x, n_y = self.x_y
        if direction == 0:
            n_y -= 1
        elif direction == 1:
            n_x += 1
        elif direction == 2:
            n_y += 1
        else:
            n_x -= 1

        return self.cloud.get(n_x, n_y)


class PointAgent(Point):
    def __init__(self, value: str, x: int, y: int, facing: Union[str, int] = 0):
        super().__init__(value, x, y)
        self.direction: int = check_direction(facing)

    def move(self, direction: Union[str, int], distance: int):
        cloud = self.cloud

        if self.cloud is not None:
            self.cloud.remove(self)

        """Direction can be NESW, UDLR, FB, or 0123"""
        if direction == "F":
            direction = self.value
        elif direction == "B":
            direction = (self.value + 2) % 4
        else:
            direction = check_direction(direction)

        if direction == 0:
            self.y -= distance
        elif direction == 1:
            self.x += distance
        elif direction == 2:
            self.y += distance
        elif direction == 3:
            self.x -= distance
        else:
            raise ValueError(f"Tried to move in an invalid direction '{direction}'")

        if cloud is not None:
            cloud.add(self)

    def turn(self, direction: Union[str, int]):
        """Direction should be L/R or +- increments"""
        if direction == "R":
            amount = 1
        elif direction == "L":
            amount = -1
        elif isinstance(direction, int):
            amount = direction
        else:
            raise ValueError(f"Tried to turn in an invalid direction '{direction}'")

        self.value = (self.value + amount) % 4


class PointGrid:
    def __init__(
            self,
            lines: Optional[Iterable[str]] = None,
            background=".",
            point_class: type[Point] = Point,
            values: list[list[str | int]] = None
    ):
        self.points: set[point_class] = set()
        if lines is not None:
            base = LineGrid(lines, pad=background)
            for p in base.find_all_not(background):
                self.points.add(
                    point_class(
                        value=base.get(*p),
                        x=p[0],
                        y=p[1]
                    )
                )
        elif values:
            for y, line in enumerate(values):
                for x, value in enumerate(line):
                    self.points.add(
                        point_class(
                            value=value,
                            x=x,
                            y=y
                        )
                    )

        self.background = background
        for point in self.points:
            point.cloud = self
        self.x_y_sorted: list[point_class] = list(sorted(self.points, key=lambda _p: (_p.x, _p.y)))
        self.y_x_sorted: list[point_class] = list(sorted(self.points, key=lambda _p: (_p.y, _p.x)))

        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self._recalc_min_max()

    @property
    def state_hash(self):
        return hash(str(self))

    def expand_11_23(self, scale: int):
        x_ordered: list[Point] = list(sorted(self.points, key=lambda p_: p_.x))
        for i in range(1, len(x_ordered)):
            dist = x_ordered[i].x - x_ordered[i - 1].x
            space = dist - 1
            if space > 0:
                for p in x_ordered[i:]:
                    p.x += space * (scale - 1)

        y_ordered: list[Point] = list(sorted(self.points, key=lambda p_: p_.y))
        for j in range(1, len(y_ordered)):
            dist = y_ordered[j].y - y_ordered[j - 1].y
            space = dist - 1
            if space > 0:
                for p in y_ordered[j:]:
                    p.y += space * (scale - 1)

    def _recalc_min_max(self) -> None:

        self.min_x = self.x_y_sorted[0].x
        self.max_x = self.x_y_sorted[-1].x
        self.min_y = self.y_x_sorted[0].y
        self.max_y = self.y_x_sorted[-1].y

    def add(self, point: Point) -> None:
        self.points.add(point)
        bisect.insort_right(self.x_y_sorted, point, key=lambda _v: (_v.x, _v.y))
        bisect.insort_right(self.y_x_sorted, point, key=lambda _v: (_v.y, _v.x))
        point.cloud = self
        self._recalc_min_max()

    def remove(self, point: Point) -> None:
        self.points.remove(point)

        start = bisect.bisect_left(self.x_y_sorted, point.x_y, key=lambda _p: _p.x_y)
        end = bisect.bisect_right(self.x_y_sorted, point.x_y, key=lambda _p: _p.x_y)
        for i in range(start, end):
            if self.x_y_sorted[i] is point:
                self.x_y_sorted.pop(i)
                break
        else:
            raise ValueError(f"Point '{point}' not present in x_y_sorted points list")

        start = bisect.bisect_left(self.y_x_sorted, (point.y, point.x), key=lambda _p: (_p.y, _p.x))
        end = bisect.bisect_right(self.y_x_sorted, (point.y, point.x), key=lambda _p: (_p.y, _p.x))
        for i in range(start, end):
            if self.y_x_sorted[i] is point:
                self.y_x_sorted.pop(i)
                break
        else:
            raise ValueError(f"Point '{point}' not present in y_x_sorted points list")

        point.cloud = None
        self._recalc_min_max()

    def get(self, x: int, y: int):
        start = bisect.bisect_left(self.x_y_sorted, (x, y), key=lambda _p: _p.x_y)
        end = bisect.bisect_right(self.x_y_sorted, (x, y), key=lambda _p: _p.x_y)
        return self.x_y_sorted[start: end]

    def get_next_in_direction(self, x: int, y: int, direction: Union[str, int]) -> list[Point]:
        direction = check_direction(direction)
        # N
        if direction == 0:
            end = bisect.bisect_left(self.x_y_sorted, (x, y), key=lambda p: p.x_y)
            y_of_next_point = self.x_y_sorted[end - 1].y
            start = bisect.bisect_left(self.x_y_sorted, (x, y_of_next_point), key=lambda p: p.x_y)
            return self.x_y_sorted[start: end]
        # E
        elif direction == 1:
            start = bisect.bisect_right(self.y_x_sorted, (y, x), key=lambda p: p.y_x)
            if start >= len(self.y_x_sorted):
                return []
            x_of_next_point = self.y_x_sorted[start].x
            end = bisect.bisect_right(self.y_x_sorted, (y, x_of_next_point), key=lambda p: p.y_x)
            return self.y_x_sorted[start: end]
        # S
        elif direction == 2:
            start = bisect.bisect_right(self.x_y_sorted, (x, y), key=lambda p: p.x_y)
            if start >= len(self.x_y_sorted):
                return []
            y_of_next_point = self.x_y_sorted[start].y
            end = bisect.bisect_right(self.x_y_sorted, (x, y_of_next_point), key=lambda p: p.x_y)
            return self.x_y_sorted[start: end]
        # W
        else:
            end = bisect.bisect_left(self.y_x_sorted, (y, x), key=lambda p: p.y_x)
            x_of_next_point = self.y_x_sorted[end - 1].x
            start = bisect.bisect_left(self.y_x_sorted, (y, x_of_next_point), key=lambda p: p.y_x)
            return self.y_x_sorted[start: end]

    def get_region(self, corner_1: tuple[int, int], corner_2: tuple[int, int]) -> set[Point]:
        x_min = min(corner_1[0], corner_2[0])
        x_max = max(corner_1[0], corner_2[0])
        y_min = min(corner_1[1], corner_2[1])
        y_max = max(corner_1[1], corner_2[1])
        x_points = set()
        y_points = set()
        for point in self.x_y_sorted:
            if point.x > x_max:
                break
            elif point.x >= x_min:
                x_points.add(point)
        for point in self.y_x_sorted:
            if point.y > y_max:
                break
            elif point.y >= y_min:
                y_points.add(point)
        return x_points.intersection(y_points)

    def __str__(self):
        grid = [[self.background for _ in range(self.min_x, self.max_x + 3)] for _ in range(self.min_y, self.max_y + 3)]
        for point in self.points:
            grid[(point.y - self.min_y) + 1][(point.x - self.min_x) + 1] = point.value
        return "\n".join(["".join(line) for line in grid])

    def __repr__(self):
        return f"{self.__class__.__name__}(num_points={len(self.points)})"

class AgentGrid(PointGrid):
    def __init__(self, lines: Iterator[str], background="."):
        self.points: set[PointAgent] = set()
        self.x_y_sorted: list[PointAgent] = []

        self.y_x_sorted: list[PointAgent] = []
        super().__init__(lines, background, point_class=PointAgent)


class Point3:
    def __init__(
            self,
            x: int,
            y: int,
            z:int,
            cloud: Optional['Point3Cloud'] = None,
            group: Optional['Point3Group'] = None
    ):
        self.x = x
        self.y = y
        self.z = z
        self.cloud = cloud
        self.group = group

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"

    def move(self, dx: int, dy: int, dz: int, skip_cloud = False):
        if self.cloud is None or skip_cloud:
            self.x += dx
            self.y += dy
            self.z += dz
        else:
            self.cloud.move_point(self, dx, dy, dz)

    @property
    def pos(self) -> [int, int, int]:
        return self.x, self.y, self.z

    def get_neighbour(self, direction: tuple[int, int, int]) -> Optional['Point3']:
        if self.cloud is None:
            raise ValueError("Point is not part of a cloud")

        if direction.count(0) < 2:
            raise ValueError("Direction cannot be a compound direction, must only be +/- 1 in one direction")

        potential_neighbour_pos = (
            self.x + direction[0],
            self.y + direction[1],
            self.z + direction[2]
        )

        return self.cloud.get_point(*potential_neighbour_pos)


class Point3Group:
    def __init__(self, p1: Point3, p2: Point3, cloud: Optional['Point3Cloud'] = None):
        self.points: list[Point3] = [p1, ]
        self.cloud = cloud

        done = False
        while not done:
            cur = self.points[-1]
            if cur.x != p2.x:
                step = sign(p2.x - cur.x)
                new_pos = (cur.x + step, cur.y, cur.z)
            elif cur.y != p2.y:
                step = sign(p2.y - cur.y)
                new_pos = (cur.x, cur.y + step, cur.z)
            else:  # cur.z != p2.z
                step = sign(p2.z - cur.z)
                new_pos = (cur.x, cur.y, cur.z + step)

            if new_pos == p2.pos:
                done = True
                self.points.append(p2)
            else:
                self.points.append(Point3(*new_pos))

        for p in self.points:
            self.cloud.add_point(p)
            p.group = self

    def __repr__(self):
        return f"Point3Group(start={self.points[0].pos}, end={self.points[-1].pos})"

    def __hash__(self):
        return hash((self.points[0].pos, self.points[-1].pos))

    def move(self, dx: int = 0, dy: int = 0, dz: int = 0):
        for point in self.points:
            point.move(dx, dy, dz)

    def get_neighbours(self, direction: tuple[int, int, int]) -> list['Point3Group']:
        neighbours: set[Point3Group] = set()
        for point in self.points:
            if new := point.get_neighbour(direction):
                if new.group is not self:
                    neighbours.add(new.group)
        return list(neighbours)

    @property
    def min_z(self) -> int:
        return min([p.z for p in self.points])


class Point3Cloud:
    def __init__(self):
        self.points: set[Point3] = set()

        self.x_y_z_sorted: list[Point3] = []
        self.z_x_y_sorted: list[Point3] = []
        self.y_x_z_sorted: list[Point3] = []
        self.sorted_lists_and_keys: list[tuple[list[Point3], Callable]] = [
            (self.x_y_z_sorted, lambda p: (p.x, p.y, p.z)),
            (self.z_x_y_sorted, lambda p: (p.z, p.x, p.y)),
            (self.y_x_z_sorted, lambda p: (p.y, p.x, p.z))
        ]

        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.min_z = 0
        self.min_z = 0

    def add_point(self, point: Point3):
        self.points.add(point)
        point.cloud = self
        for sorted_list, key in self.sorted_lists_and_keys:
            bisect.insort(sorted_list, point, key=key)
        self._recalc_min_max()

    def remove_point(self, point: Point3):
        self.points.remove(point)
        for sorted_list, key in self.sorted_lists_and_keys:
            start = bisect.bisect_left(sorted_list, key(point), key=key)
            for i in range(start, len(sorted_list)):
                if sorted_list[i] is point:
                    sorted_list.pop(i)
                    break
            else:
                raise ValueError("Point not in the list")

    def _recalc_min_max(self):
        if len(self.points) == 0:
            self.min_x = 0
            self.max_x = 0
            self.min_y = 0
            self.max_y = 0
            self.min_z = 0
            self.min_z = 0
        else:
            self.min_x = self.x_y_z_sorted[0].x
            self.max_x = self.x_y_z_sorted[-1].x
            self.min_y = self.y_x_z_sorted[0].y
            self.max_y = self.y_x_z_sorted[-1].y
            self.min_z = self.z_x_y_sorted[0].z
            self.min_z = self.z_x_y_sorted[-1].z

    def move_point(self, point: Point3, dx=0, dy=0, dz=0):
        self.remove_point(point)
        point.move(dx, dy , dz, skip_cloud=True)
        self.add_point(point)

    def get_point(self, x: int, y: int, z: int) -> Optional[Point3]:
        sorted_list, key = (self.z_x_y_sorted, lambda p: (p.z, p.x, p.y))
        i = bisect.bisect_left(sorted_list, (z, x, y), key=key)
        if (i < len(self.z_x_y_sorted)) and (self.z_x_y_sorted[i].pos == (x, y, z)):
            return self.z_x_y_sorted[i]
        else:
            return None


class Node:
    def __init__(self):
        self.connections: set[Node] = set()
        self.value: Any = None

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value}, connections={len(self.connections)})"


class NodeWithDistance:
    def __init__(self):
        self.connections: dict[NodeWithDistance, int] = {}

    def __repr__(self):
        return f"{self.__class__.__name__}(connections={len(self.connections)})"


def sign(n):
  if n<0: return -1
  elif n>0: return 1
  else: return 0


def manhattan_distance(p1: Union[tuple[int, int], Point], p2: Union[tuple[int, int], Point]) -> int:
    if isinstance(p1, Point):
        x1, y1 = p1.x, p1.y
    else:
        x1, y1 = p1
    if isinstance(p2, Point):
        x2, y2 = p2.x, p2.y
    else:
        x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def check_direction(direction: Union[str, int]) -> int:
    """
    raises: ValueError if direction is not valid.
    """
    if isinstance(direction, int) and 0 <= direction <= 3:
        return direction
    else:
        try:
            return VALID_DIRECTIONS.index(direction) % 4
        except IndexError:
            pass

    raise ValueError(f"Direction '{direction}' is not valid")


def get_direction(coord_1: tuple[int, int], coord_2: tuple[int, int]) -> int:
    if coord_2[0] > coord_1[0]:
        return 1
    elif coord_2[1] > coord_1[1]:
        return 2
    elif coord_2[0] < coord_1[0]:
        return 3
    elif coord_2[1] < coord_1[1]:
        return 0
