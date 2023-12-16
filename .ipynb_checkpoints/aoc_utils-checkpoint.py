import bisect
import logging
from pathlib import Path
from typing import Union, Optional, Type, Iterator, Any, Generator, Callable


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


class LineGrid:
    def __init__(self, lines: Iterator[str], pad: str = "."):
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

    def get_neighbour(self, x: int, y: int, direction: str, wrap=False) -> tuple[Union[str, int], int, int]:
        """
        Directions: any 1 or 2 char combination of N, W, S, W or U, D, L, R
        returns: neighbour value, x, y
        """
        if "N" in direction or "U" in direction:
            y -= 1
        if "E" in direction or "R" in direction:
            x += 1
        if "S" in direction or "D" in direction:
            y += 1
        if "W" in direction or "L" in direction:
            x -= 1
        return self.get(x, y, wrap), x, y

    def __str__(self):
        return "\n".join(["".join(line) for line in self.lines])


class Point:
    def __init__(self, value: Union[str, int], x: int, y: int, cloud: Optional['PointCloud'] = None):
        self.value = value
        self.x = x
        self.y = y
        self.cloud = cloud

    @property
    def coord(self) -> tuple[int, int]:
        return self.x, self.y

    def __repr__(self) -> str:
        return f"Point(value={repr(self.value)}, x={self.x}, y={self.y})"


class PointAgent(Point):
    valid_directions = ["N", "E", "S", "W", "U", "D", "L", "R", "0", "1", "2", "3", 0, 1, 2, 3]

    def __init__(self, facing: str, x: int, y: int):
        if facing not in self.valid_directions:
            raise ValueError(f"'facing' must be a valid direction in {self.valid_directions}")
        direction: int = self.valid_directions.index(facing) % 4  # Convert direction str to int
        super().__init__(direction, x, y)

    def move(self, direction: Union[str, int], distance: int):
        if self.cloud is not None:
            self.cloud.remove(self)

        """Direction can be NESW, UDLR, FB, or 0123"""
        if isinstance(direction, int) and (0 <= direction <= 3):
            pass
        elif direction == "F":
            direction = self.value
        elif direction == "B":
            direction = (self.value + 2) % 4
        elif direction in self.valid_directions:
            direction = self.valid_directions.index(direction) % 4
        else:
            raise ValueError(f"'direction' must be a valid direction in {self.valid_directions}")

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

    def get_neighbour(self, direction: Union[int, str]) -> Optional['Point']:
        if self.cloud is None:
            raise ValueError("Point does not have a cloud")

        if isinstance(direction, str):
            direction = self.valid_directions.index(direction) % 4

        if direction == 0 or direction == 2:
            def axis_key(p: Point):
                return p.x
            start = bisect.bisect_left(self.cloud.x_sorted, self.x)
            end = bisect.bisect_right(self.cloud.x_sorted, self.x)
            possible_neighbours = self.cloud.x_sorted[start: end]
        else:
            def axis_key(p: Point):
                return p.y
            start = bisect.bisect_left(self.cloud.y_sorted, self.y)
            end = bisect.bisect_right(self.cloud.y_sorted, self.y)
            possible_neighbours = self.cloud.y_sorted[start: end]

        if direction == 0 or direction == 3:
            target = axis_key(self) - 1
        else:
            target = axis_key(self) + 1

        for n in possible_neighbours:
            if axis_key(n) == target:
                return n
        return None


class PointCloud:
    def __init__(self, lines: Iterator[str], background=".", point_class: type[Point] = Point):
        base = LineGrid(lines, pad=background)
        self.points: set[point_class] = set([
            point_class(
                value=base.get(*p),
                x=p[0],
                y=p[1],
                cloud=self
            ) for p in base.find_all_not(".")
        ])
        self.x_sorted: list[point_class] = list(sorted(self.points, key=lambda p: p.x))
        self.y_sorted: list[point_class] = list(sorted(self.points, key=lambda p: p.x))

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

    def add(self, point: Point):
        self.points.add(point)
        self.x_sorted.insert(
            bisect.bisect_right(self.x_sorted, point.x, key=lambda v: v.x),
            point
        )
        self.y_sorted.insert(
            bisect.bisect_right(self.y_sorted, point.y, key=lambda v: v.y),
            point
        )

    def remove(self, p: Point):
        self.points.remove(p)
        self.x_sorted.remove(p)
        self.y_sorted.remove(p)


class AgentCloud(PointCloud):
    def __init__(self, lines: Iterator[str], background="."):
        super().__init__(lines, background, point_class=PointAgent)


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
