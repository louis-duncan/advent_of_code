from pathlib import Path
from typing import Union, Optional


def raw_input(input_path: Path = Path("input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read().strip()
    return data.strip()


def load_instructions() -> list[tuple[str, int]]:
    instructions: list[tuple[str, int]] = []

    for line in raw_input().split("\n"):
        instruction, value = line.strip().split(" ")
        instructions.append((instruction, int(value)))

    return instructions


def part_1(instructions: Optional[list[tuple[str, int]]] = None) -> int:
    if instructions is None:
        instructions = load_instructions()
    states: set[int] = set()

    acc = 0
    prc = 0

    while True:
        current_state = prc
        if current_state in states:
            break
        else:
            states.add(current_state)

        instruction, value = instructions[prc]
        if instruction == "acc":
            acc += value
            prc += 1
        elif instruction == "nop":
            prc += 1
        elif instruction == "jmp":
            prc += value
        else:
            raise ValueError(f"Unexpected instruction '{instruction}'")

    return acc


def completes(instructions: Optional[list[tuple[str, int]]] = None) -> (bool, int):
    if instructions is None:
        instructions = load_instructions()
    states: set[int] = set()

    acc = 0
    prc = 0
    next_instruction = len(instructions)

    while True:
        current_state = prc
        if current_state in states:
            return False, acc
        else:
            states.add(current_state)

        try:
            instruction, value = instructions[prc]
        except IndexError:
            return False, acc

        if instruction == "acc":
            acc += value
            prc += 1
        elif instruction == "nop":
            prc += 1
        elif instruction == "jmp":
            prc += value
        else:
            raise ValueError(f"Unexpected instruction '{instruction}'")

        if prc == next_instruction:
            return True, acc


def part_2() -> Union[int, str]:
    instructions: list[tuple[str, int]] = load_instructions()

    prc = 0
    acc = 0
    past_states: set[int] = set()
    term_instruction = len(instructions)

    change_location = 0
    past_states_at_change: set[int] = set()
    state_at_change: Optional[tuple[int, int]] = None
    change_tried = False

    while True:
        if prc in past_states or prc > term_instruction:
            if state_at_change is None:
                print("Hit dead end")
                return "..."
            else:
                prc, acc = state_at_change
                past_states = past_states_at_change
                state_at_change = None
                change_tried = True

        instruction, value = instructions[prc]
        past_states.add(prc)

        if instruction == "acc":
            acc += value
            prc += 1
        else:
            if state_at_change or change_tried:
                # We've made a change, run as normal
                if instruction == "nop":
                    prc += 1
                elif instruction == "jmp":
                    prc += value
            else:
                # Save the state and invert the behaviour
                state_at_change = (prc, acc)
                past_states_at_change = past_states.copy()
                change_location = prc
                if instruction == "jmp":
                    prc += 1
                elif instruction == "nop":
                    prc += value
            change_tried = False

        if prc == term_instruction:
            break


    print(change_location)
    return acc


if __name__ == "__main__":
    load_instructions()

    print("Part 1:", part_1())
    print()
    print("Part 2:", part_2())
