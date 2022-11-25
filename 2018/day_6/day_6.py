from typing import Optional, List


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def pos(self):
        return self.x, self.y

    def point_distance(self, other: 'Point') -> int:
        return self.pos_distance(*other.pos)

    def pos_distance(self, x: int, y: int) -> int:
        return abs(x - self.x) + abs(y - self.y)

    @classmethod
    def from_str(cls, point_str: str) -> 'Point':
        x_str, y_str = point_str.split(", ")
        return cls(int(x_str), int(y_str))

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"


class Node(Point):
    next_node_id = 0

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        self.id = Node.next_node_id
        Node.next_node_id += 1

        self.points: List[Point] = []
        self.is_closed_region = True

    def __repr__(self):
        return f"Node(x={self.x}, y={self.y})"


def part_1():
    with open("input.txt", "r") as fh:
        nodes = [Node.from_str(line.strip()) for line in fh]

    x_min = min([p.x for p in nodes])
    y_min = min([p.y for p in nodes])
    x_max = max([p.x for p in nodes])
    y_max = max([p.y for p in nodes])

    grid_x_range = x_min - 1, x_max + 1
    grid_y_range = y_min - 1, y_max + 1

    # Make points, assign each to the closest node
    for x in range(*grid_x_range):
        for y in range(*grid_y_range):
            border_point = False
            if x == grid_x_range[0] or x == grid_x_range[1] or y == grid_y_range[0] or x == grid_y_range[1]:
                border_point = True

            new_point = Point(x, y)
            nodes_by_distance = list(
                sorted(
                    nodes,
                    key=lambda p: p.point_distance(new_point)
                )
            )

            if new_point.point_distance(nodes_by_distance[0]) < new_point.point_distance(nodes_by_distance[1]):
                nodes_by_distance[0].points.append(new_point)
                if border_point:
                    nodes_by_distance[0].is_closed_region = False

    print(max([len(n.points) for n in nodes]))


def part_2():
    with open("input.txt", "r") as fh:
        nodes = [Node.from_str(line.strip()) for line in fh]

    x_min = min([p.x for p in nodes])
    y_min = min([p.y for p in nodes])
    x_max = max([p.x for p in nodes])
    y_max = max([p.y for p in nodes])

    grid_x_range = x_min - 1, x_max + 1
    grid_y_range = y_min - 1, y_max + 1

    points_in_region = 0

    # Make points, assign each to the closest node
    max_distance = 10000
    for x in range(*grid_x_range):
        for y in range(*grid_y_range):
            tot = 0
            for node in nodes:
                tot += node.pos_distance(x, y)
                if tot >= max_distance:
                    break
            if tot < max_distance:
                points_in_region += 1
    print(points_in_region)


if __name__ == '__main__':
    part_2()
