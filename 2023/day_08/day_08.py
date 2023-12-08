import re
from pathlib import Path
from typing import Union, Iterator, Optional, Type, Any

"""
https://adventofcode.com/2023/day/8
"""


class Node:
    all_nodes: dict[str, 'Node'] = {}

    def __init__(self, name: str, left: str, right: str):
        self.name = name
        self._left_name = left
        self._right_name = right
        self.is_start_node = name.endswith("A")
        self.is_end_node = name.endswith("Z")

    @property
    def left(self) -> 'Node':
        try:
            return self.all_nodes[self._left_name]
        except KeyError:
            raise ValueError(f"Node '{self._left_name}' does not exist")

    @property
    def right(self) -> 'Node':
        try:
            return self.all_nodes[self._right_name]
        except KeyError:
            raise ValueError(f"Node '{self._right_name}' does not exist")

    @classmethod
    def add_node(cls, name, left, right):
        cls.all_nodes[name] = Node(name, left, right)

    def __repr__(self):
        return f"Node(name={repr(self.name)})"


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


def part_1() -> Union[int, str]:
    lines = list(input_lines("input.txt"))
    for line in lines[2:]:
        node_strs = re.findall(r"\w{3}", line)
        Node.add_node(*node_strs)

    current_location: Node = Node.all_nodes['AAA']
    count = 0

    directions = lines[0].strip()
    while current_location.name != "ZZZ":
        for direction in directions:
            count += 1
            if direction == "L":
                current_location = current_location.left
            else:
                current_location = current_location.right
            if current_location.name == "ZZZ":
                break
    return count


def part_2() -> Union[int, str]:
    Node.all_nodes.clear()

    lines = list(input_lines("test_input.txt"))
    for line in lines[2:]:
        node_strs = re.findall(r"\w{3}", line)
        Node.add_node(*node_strs)

    start_locations: list[Node] = [n for n in Node.all_nodes.values() if n.is_start_node]
    directions = lines[0].strip()
    len_directions = len(directions)

    cycles: dict[Node, dict[str, Union[int, dict[tuple[str, int], int], tuple[str, int]]]] = {}

    for start in start_locations:
        #                 node step
        states: dict[tuple[str, int], int] = {}
        count = 0
        has_looped = False
        current = start
        state = ("", 0)
        while not has_looped:
            step = count % len_directions
            if directions[step] == "L":
                current = current.left
            else:
                current = current.right
            state = (current.name, step)
            if state in states:
                has_looped = True
            else:
                states[state] = count
                count += 1
        cycle_start_node = Node.all_nodes[state[0]]

        cycle_nodes = [Node.all_nodes[state[0]] for state in states]
        for n in cycle_nodes:
            if n.is_end_node:
                goal_node = n
                break
        else:
            raise ValueError("No end node in cycle")

        cycles[start] = {
            'cycle_end_count': count,
            'all_nodes': cycle_nodes,
            'cycle_start_node': cycle_start_node,
            'goal_node': goal_node
        }

    for node, cycle in cycles.items():
        assert len([n for n in cycle['all_nodes'] if n.is_end_node]) >= 1

    start_offsets: list[int] = []
    goal_offsets_from_cycle_start: list[int] = []
    cycle_lengths: list[int] = []

    for cycle in cycles.values():
        all_nodes = cycle['all_nodes']
        start_node = cycle['cycle_start_node']
        goal_node = cycle['goal_node']
        start_offsets.append(all_nodes.index(start_node))
        goal_offsets_from_cycle_start.append(all_nodes.index(goal_node) - all_nodes.index(start_node))
        cycle_lengths.append(len(all_nodes) - all_nodes.index(start_node))
    pass



    pass

    return count


if __name__ == "__main__":
    print("Part 1:", part_1())
    print()
    print("Part 2:", part_2())
