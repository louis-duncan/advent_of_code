from math import inf
from typing import List, Union, Optional


class Node:
    def __init__(self, x: int, y: int, value: int):
        self.x = x
        self.y = y
        self.value = value
        self.connections: List[Node] = []
        self.visited = False
        self.distance: Union[int, float] = inf
        self.visited_from: Optional[Node] = None

    def __repr__(self):
        return f"Node(x={self.x}, y={self.y}, value={self.value}, #connections={len(self.connections)}, distance={self.distance})"


def part_1():
    with open("input.txt", "r") as fh:
        data = [list(line.strip()) for line in fh.readlines()]

    nodes_grid: List[List[Node]] = []
    nodes: List[Node] = []
    start_node = None
    end_node = None
    for y in range(len(data)):
        row = []
        for x in range(len(data[0])):
            value = ord(data[y][x])
            new_node = Node(x, y, value)
            row.append(new_node)
            nodes.append(new_node)
            if value == 83:  # "S"
                start_node = new_node
                new_node.value = ord("a")
                start_node.distance = 0
            elif value == 69:  # "E"
                end_node = new_node
                new_node.value = ord("z") + 1
        nodes_grid.append(row)

    pass

    for x in range(len(nodes_grid[0])):
        for y in range(len(nodes_grid)):
            checks = []
            cur_node = nodes_grid[y][x]
            if x > 0:
                checks.append((x - 1, y))
            if x < len(nodes_grid[0]) - 1:
                checks.append((x + 1, y))
            if y > 0:
                checks.append((x, y - 1))
            if y < len(data) - 1:
                checks.append((x, y + 1))

            for cx, cy in checks:
                check_node = nodes_grid[cy][cx]
                if nodes_grid[cy][cx].value <= cur_node.value + 1:
                    cur_node.connections.append(check_node)

    nodes_under_consideration: List[Node] = [start_node]
    while len(nodes_under_consideration) > 0:
        new_considerations: List[Node] = []
        for cur_node in nodes_under_consideration:
            for pos_node in cur_node.connections:
                if (not pos_node.visited) or (pos_node.distance > cur_node.distance + 1):
                    pos_node.visited = True
                    pos_node.distance = cur_node.distance + 1
                    pos_node.visited_from = cur_node
                    if pos_node not in new_considerations:
                        new_considerations.append(pos_node)
        nodes_under_consideration = new_considerations

    print(end_node.distance)

    pass


def part_2():
    with open("input.txt", "r") as fh:
        data = [list(line.strip()) for line in fh.readlines()]

    nodes_grid: List[List[Node]] = []
    nodes: List[Node] = []
    start_node = None
    end_node = None
    for y in range(len(data)):
        row = []
        for x in range(len(data[0])):
            value = ord(data[y][x])
            new_node = Node(x, y, value)
            row.append(new_node)
            nodes.append(new_node)
            if value == 83:  # "S"
                new_node.value = ord("a")
            elif value == 69:  # "E"
                new_node.value = ord("z") + 1
                new_node.distance = 0
                start_node = new_node
        nodes_grid.append(row)

    pass

    for x in range(len(nodes_grid[0])):
        for y in range(len(nodes_grid)):
            checks = []
            cur_node = nodes_grid[y][x]
            if x > 0:
                checks.append((x - 1, y))
            if x < len(nodes_grid[0]) - 1:
                checks.append((x + 1, y))
            if y > 0:
                checks.append((x, y - 1))
            if y < len(data) - 1:
                checks.append((x, y + 1))

            for cx, cy in checks:
                check_node = nodes_grid[cy][cx]
                if nodes_grid[cy][cx].value >= cur_node.value - 1:
                    cur_node.connections.append(check_node)

    nodes_under_consideration: List[Node] = [start_node]
    done = False
    while len(nodes_under_consideration) > 0:
        new_considerations: List[Node] = []
        for cur_node in nodes_under_consideration:
            if cur_node.value == 97:  # "a"
                print(cur_node)
                done = True
                break
            for pos_node in cur_node.connections:
                if (not pos_node.visited) or (pos_node.distance > cur_node.distance + 1):
                    pos_node.visited = True
                    pos_node.distance = cur_node.distance + 1
                    pos_node.visited_from = cur_node
                    if pos_node not in new_considerations:
                        new_considerations.append(pos_node)
        if done:
            break
        nodes_under_consideration = new_considerations

    pass


if __name__ == '__main__':
    part_2()
