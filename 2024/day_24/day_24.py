import dataclasses
import itertools
import operator
import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/24
"""

_INPUT_PATH = INPUT_PATH  # _TEST


@dataclasses.dataclass
class Wire:
    name: str
    value: int = 0
    updated: bool = False
    connected_inputs: list['Gate'] = dataclasses.field(default_factory=list)
    connected_output: list['Gate'] = dataclasses.field(default_factory=list)

    def __hash__(self):
        return hash(self.name)


class Gate:
    def __init__(self, op: Callable[[int, ...], int], input_1: Wire, input_2: Wire, output: Wire):
        if input_1.name == "x00":
            pass
        self.op = op
        self.input_1 = input_1
        self.input_2 = input_2
        self.output = output
        self.input_1.connected_inputs.append(self)
        self.input_2.connected_inputs.append(self)
        self.output.connected_output.append(self)

    def update(self):
        self.output.value = self.op(self.input_1.value, self.input_2.value)
        self.output.updated = True


def part_1() -> Union[int, str]:
    ops: dict[str, Callable[[int, ...], int]] = {
        "AND": operator.and_,
        "OR": operator.or_,
        "XOR": operator.xor
    }

    wires: dict[str, Wire] = {}
    gates = []
    lines = list(input_lines(_INPUT_PATH))
    i = 0
    to_update: list[Wire] = []
    for i, line in enumerate(lines):
        if line == "":
            break
        wire_name, v_str = line.strip().split(": ")
        wires[wire_name] = Wire(wire_name, int(v_str))
        to_update.append(wires[wire_name])

    for line in lines[i + 1:]:
        parts = re.findall(r"\w+", line)
        for w in (parts[0], parts[2], parts[3]):
            if w not in wires:
                wires[w] = Wire(w, 0)

        gates.append(
            Gate(
                op=ops[parts[1]],
                input_1=wires[parts[0]],
                input_2=wires[parts[2]],
                output=wires[parts[3]]
            )
        )

    while len(to_update) > 1:
        new_activations: list[Wire] = []
        a: Wire
        b: Wire
        processed: set[Wire] = set()
        for a, b in itertools.combinations(to_update, 2):
            if not a.connected_inputs:
                processed.add(a)
                continue
            if not b.connected_inputs:
                processed.add(b)
            for g in a.connected_inputs:
                if g in b.connected_inputs:
                    g.update()
                    new_activations.append(g.output)
                    processed.add(a)
                    processed.add(b)
        for w in processed:
            to_update.remove(w)
        to_update = to_update + new_activations

    z_named = sorted([w for w in wires.values() if w.name.startswith("z")], key=lambda x: x.name)
    # for w in sorted([w for w in wires.values()], key=lambda x: x.name):
    #     print(w.name, w.value)
    bits_str = "".join(str(z.value) for z in reversed(z_named))
    return int(bits_str, 2)


def part_2() -> Union[int, str]:
    ...


if __name__ == "__main__":
    p1_start = time.time()
    part_1_answer = part_1()
    p1_duration = time.time() - p1_start
    if part_1_answer is not None:
        print(f"Part 1 ({p1_duration * 1000:.2f}ms):", part_1_answer)
        pyperclip.copy(part_1_answer)
    print()

    p2_start = time.time()
    part_2_answer = part_2()
    p2_duration = time.time() - p2_start
    if part_2_answer is not None:
        print(f"Part 2 ({p2_duration * 1000:.2f}ms):", part_2_answer)
        pyperclip.copy(part_2_answer)
