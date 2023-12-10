import logging
from pathlib import Path
from typing import Union, Optional, Type, Iterator, Any


def raw_input(input_path: Union[Path, str] = Path("test_input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read()
    return data


def input_lines(
        input_path: Union[Path, str] = Path("test_input.txt"),
        convert_type: Optional[Type] = None
) -> Iterator[Any]:
    for line in raw_input(input_path).strip().split("\n"):
        if convert_type is None:
            yield line.strip()
        else:
            yield convert_type(line.strip())


class LineGrid:
    def __init__(self, lines: Iterator[str], pad="."):
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

    def find(self, value: Any) -> tuple[int, int]:
        for y in range(self.height):
            for x in range(self.width):
                if self.__quick_get(x, y) == value:
                    return x, y
        else:
            raise ValueError(f"{value} is not in grid")

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
