import re
from typing import List


def do_move_9000(n: int, stack_1: List[str], stack_2: List[str]):
    for _ in range(n):
        stack_2.append(stack_1.pop())


def do_move_9001(n: int, stack_1: List[str], stack_2: List[str]):
    block = stack_1[-n:]
    for _ in range(n):
        stack_1.pop()
    stack_2 += block


def main():
    stacks = []
    moves = []
    with open("input.txt", "r") as fh:
        # Load Crates
        load_crates = True
        for line in fh.readlines():
            if load_crates:
                if line.startswith(" 1"):
                    load_crates = False
                    continue
                line = line.rstrip()
                parts = [line[i: i+4].strip("[] ") for i in range(0, len(line), 4)]

                if len(parts) > len(stacks):
                    for _ in range(len(parts) - len(stacks)):
                        stacks.append([])

                for i, crate in enumerate(parts):
                    if crate != "":
                        stacks[i].insert(0, crate)
            else:
                line = line.strip()
                if line == "":
                    pass
                else:
                    moves.append([int(i) for i in re.findall(r"\d.?", line)])

        # Do Moves
        for n, s1, s2 in moves:
            do_move_9001(n, stacks[s1 - 1], stacks[s2 - 1])

    for stack in stacks:
        print(stack[-1], end="")


if __name__ == '__main__':
    main()
