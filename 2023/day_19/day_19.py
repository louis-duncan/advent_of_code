import operator
import re
from typing import Callable

from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2023/day/19
"""

OPS = {
    ">": operator.gt,
    "<": operator.lt,
    "": None
}

class Action:
    def __init__(self, target: str, op: str = "", key: str = "", value: int = 0):
        self.op: Optional[Callable[[int, int], bool]] = OPS[op]
        self.key = key
        self.value = value
        self.target = target

    def __call__(self, item: dict[str, int]) -> Optional[str]:
        if self.op is None:
            return self.target
        else:
            if self.key in item:
                if self.op(item[self.key], self.value):
                    return self.target
                else:
                    return None
            else:
                return None

class Workflow:
    def __init__(self, name: str, action_str: str):
        self.name = name
        self.actions_list: list[Action] = []
        """a<2006:qkq"""
        for action in action_str.split(','):
            if ":" in action:
                key, op, value, target = re.match(r"(\w+)([<>])(\d+):(\w+)", action).groups()
                value = int(value)
                new_action = Action(
                    target=target,
                    op=op,
                    key=key,
                    value=value
                )
            else:
                new_action = Action(
                    target=action
                )
            self.actions_list.append(new_action)

    def process(self, item: dict[str, int]) -> str:
        """Returns the str name of the next flow"""
        for action in self.actions_list:
            res = action(item)
            if res:
                return res
        else:
            raise ValueError(f"No action triggered for item '{item}' in workflow '{self.name}'")


def part_1() -> Union[int, str]:
    workflows: dict[str, 'Workflow'] = {}

    action_lines, item_lines = grouped_input_lines("input.txt")
    for line in action_lines:
        name, actions = re.match(r"(\w+){(.*)}", line).groups()
        workflows[name] = Workflow(name, actions)

    accepted = []
    rejected = []
    for line in item_lines:#
        groups = re.findall(r"(\w+)=(\d+)", line)
        item = {k: int(v) for k, v in groups}

        done = False
        flow = workflows['in']
        while not done:
            dest = flow.process(item)
            if dest == "A":
                accepted.append(item)
                done = True
            elif dest == "R":
                rejected.append(item)
                done = True
            else:
                flow = workflows[dest]

    return sum([sum(i.values()) for i in accepted])


def part_2() -> Union[int, str]:
    ...


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
