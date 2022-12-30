from typing import List, Union, Tuple, Set


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos_history: List[Tuple[int, int]] = []
        self.log_pos()

    @property
    def pos(self):
        return self.x, self.y

    def log_pos(self):
        self.pos_history.append((self.x, self.y))

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"


def get_signed_unit(n: int) -> int:
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0


def move_point(point: Point, move: Tuple[str, int]):
    match move[0]:
        case "R":
            point.x += move[1]
        case "L":
            point.x -= move[1]
        case "U":
            point.y += move[1]
        case "D":
            point.y -= move[1]
        case _:
            raise ValueError("Unknown direction")


def move_follower(follower: Point, target: Point):
    done = False
    while not done:
        dx = target.x - follower.x
        dy = target.y - follower.y
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        if abs_dx <= 1 and abs_dy <= 1:
            done = True
        elif (dx != 0 and abs_dy > 1) or (abs_dx > 1 and dy != 0):
            follower.x += get_signed_unit(dx)
            follower.y += get_signed_unit(dy)
            follower.log_pos()
        else:
            if abs_dx > 1:
                follower.x += get_signed_unit(dx)
                follower.log_pos()
            elif abs_dy > 1:
                follower.y += get_signed_unit(dy)
                follower.log_pos()


def move_followers(points: List[Point]):
    done = False
    while not done:
        done = True
        for i in range(len(points) - 1):
            moved = False
            target = points[i]
            follower = points[i + 1]
            dx = target.x - follower.x
            dy = target.y - follower.y
            abs_dx = abs(dx)
            abs_dy = abs(dy)
            if abs_dx <= 1 and abs_dy <= 1:
                pass
            elif (dx != 0 and abs_dy > 1) or (abs_dx > 1 and dy != 0):
                follower.x += get_signed_unit(dx)
                follower.y += get_signed_unit(dy)
                done = False
                moved = True
                if follower is points[-1]:
                    follower.log_pos()
            else:
                if abs_dx > 1:
                    follower.x += get_signed_unit(dx)
                    done = False
                    moved = True
                    if follower is points[-1]:
                        follower.log_pos()
                elif abs_dy > 1:
                    follower.y += get_signed_unit(dy)
                    done = False
                    moved = True
                    if follower is points[-1]:
                        follower.log_pos()
            if not moved:
                break
            #print_state(points)
            pass


def print_tail_trail(pos_history: Set[Tuple[int, int]]):
    x_min = min([x for x, y in pos_history])
    x_max = max([x for x, y in pos_history])
    y_min = min([y for x, y in pos_history])
    y_max = max([y for x, y in pos_history])

    grid = []

    for y in range(y_min - 1, y_max + 1):
        row = []
        for x in range(x_min - 1, x_max + 1):
            row.append(".")
        grid.append(row)

    grid[0][0] = "s"

    for x, y in pos_history:
        grid[y][x] = "#"

    output_lines = []
    for y in range(y_min - 1, y_max + 1):
        line = ""
        for x in range(x_min - 1, x_max + 1):
            line += grid[y][x]
        output_lines.append(line)
    print("\n".join(reversed(output_lines)))


def print_state(points: List[Point]):
    x_min = min([p.x for p in points] + [0])
    x_max = max([p.x for p in points] + [0])
    y_min = min([p.y for p in points] + [0])
    y_max = max([p.y for p in points] + [0])

    grid = []
    for y in range(y_min, y_max + 1):
        row = []
        for x in range(x_min, x_max + 1):
            row.append(".")
        grid.append(row)

    grid[0][0] = "s"
    for i, point in reversed(list(enumerate(points))):
        grid[point.y][point.x] = str(i)

    output_lines = []
    for y in range(y_min, y_max + 1):
        line = ""
        for x in range(x_min, x_max + 1):
            line += grid[y][x]
        output_lines.append(line)
    print()
    print("\n".join(reversed(output_lines)))


def main():
    moves: List[Tuple[str, int]] = []
    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            line_parts = line.strip().split()
            moves.append((line_parts[0], int(line_parts[1])))

    points = [Point() for i in range(10)]

    for move in moves:
        move_point(points[0], move)
        #print_state(points)
        pass
        move_followers(points)

    print_tail_trail(set(points[-1].pos_history))
    print(len(set(points[-1].pos_history)))


if __name__ == '__main__':
    main()
