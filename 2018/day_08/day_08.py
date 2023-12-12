from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2018/day/8
"""


class Node:
    def __init__(self, children: list['Node'], metadata: list[int]):
        self.children: list['Node'] = children
        self.metadata: list[int] = metadata

    def sum_metadata(self) -> int:
        total = sum(self.metadata)
        for child in self.children:
            total += child.sum_metadata()
        return total

    def value_p2(self) -> int:
        if len(self.children) == 0:
            return sum(self.metadata)
        else:
            total = 0
            for m in self.metadata:
                try:
                    total += self.children[m - 1].value_p2()
                except IndexError:
                    pass
            return total

    def __repr__(self):
        return f"Node(num_children={len(self.children)}, metadata={repr(self.metadata)}"


def load_node(data: list[int]) -> tuple[Node, int]:
    num_children = data[0]
    num_meta_data = data[1]

    pos = 2
    children: list[Node] = []
    for _ in range(num_children):
        child, child_len = load_node(data[pos:])
        children.append(child)
        pos += child_len

    new_node = Node(children, data[pos: pos + num_meta_data])
    pos += num_meta_data
    return new_node, pos


def part_1() -> Union[int, str]:
    data = [int(n) for n in raw_input("input.txt").strip().split(" ")]
    root, _ = load_node(data)
    return root.sum_metadata()


def part_2() -> Union[int, str]:
    data = [int(n) for n in raw_input("input.txt").strip().split(" ")]
    root, _ = load_node(data)
    return root.value_p2()


if __name__ == "__main__":
    part_1_answer = part_1()
    if part_1_answer is not None:
        print("Part 1:", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    part_2_answer = part_2()
    if part_2_answer is not None:
        print("Part 2:", part_2_answer)
        pyperclip.copy(part_2_answer)
