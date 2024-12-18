import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2024/day/17
"""

_INPUT_PATH = INPUT_PATH # _TEST


class Registers:
    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c
        self.inst = 0
        self._step_size = 2
        self.output_buffer: list[int] = []

    def get_operator(self, opcode: int) -> Callable:
        match opcode:
            case 0:
                return self.adv
            case 1:
                return self.bxl
            case 2:
                return self.bst
            case 3:
                return self.jnz
            case 4:
                return self.bxc
            case 5:
                return self.out
            case 6:
                return self.bdv
            case 7:
                return self.cdv
            case _:
                raise ValueError(f"Invalid opcode {opcode}")

    def get_combo_op(self, value: int) -> int:
        match value:
            case value if 0 <= value <= 3:
                return value
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise ValueError(f"Invalid combo value {value}")

    def adv(self, operand: int):
        self.a = self.a // (2 ** self.get_combo_op(operand))
        self.inst += self._step_size

    def bxl(self, operand: int):
        self.b = self.b ^ operand
        self.inst += self._step_size

    def bst(self, operand: int):
        self.b = self.get_combo_op(operand) % 8
        self.inst += self._step_size

    def jnz(self, operand: int):
        if self.a != 0:
            self.inst = operand
        else:
            self.inst += self._step_size

    def bxc(self, _: int):
        self.b = self.b ^ self.c
        self.inst += self._step_size

    def out(self, operand: int):
        self.output_buffer.append(self.get_combo_op(operand) % 8)
        # print(self.a, self.b, self.c, self.get_combo_op(operand) % 8)
        self.inst += self._step_size

    def bdv(self, operand: int):
        self.b = self.a // (2 ** self.get_combo_op(operand))
        self.inst += self._step_size

    def cdv(self, operand: int):
        self.c = self.a // (2 ** self.get_combo_op(operand))
        self.inst += self._step_size


def run_program(a: int, limit: int=inf) -> str:
    nums = [int(n) for n in re.findall(r"\d+", raw_input(_INPUT_PATH), flags=re.MULTILINE)]
    registers = Registers(a, 0, 0)
    program = nums[3:]

    len_prog = len(program)
    while registers.inst < len_prog and len(registers.output_buffer) < limit:
        op = registers.get_operator(program[registers.inst])
        op(program[registers.inst + 1])

    return ",".join([str(n) for n in registers.output_buffer])


def part_1() -> Union[int, str]:
    nums = [int(n) for n in re.findall(r"\d+", raw_input(_INPUT_PATH), flags=re.MULTILINE)]
    return run_program(nums[0])


def part_2() -> Union[int, str]:
    def get_options(_n: int) -> set[int]:
        _options = set(range(_n * 8, (_n * 8) + 8))
        try:
            _options.remove(0)
        except KeyError:
            pass
        return _options

    def get_output(_n: int) -> int:
        return ((((_n % 8) ^ 3) ^ 5) ^ (_n // (2 ** ((_n % 8) ^ 3)))) % 8

    def get_next_a(_n: int) -> int:
        return _n // 8

    nums = [int(n) for n in re.findall(r"\d+", raw_input(_INPUT_PATH), flags=re.MULTILINE)]
    program = nums[3:]

    options = {0,}
    for n in reversed(program):
        new_options = set()
        for o in options:
            for p in get_options(o):
                if get_output(p) == n:
                    new_options.add(p)
        options = new_options

    expected = ",".join([str(n) for n in program])
    for o in sorted(options):
        result = run_program(o, limit=len(program))
        if result == expected:
            return o


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
