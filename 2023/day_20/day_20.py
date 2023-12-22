from abc import ABC, abstractmethod
from collections import deque

from aoc_utils import *

import pyperclip

"""
https://adventofcode.com/2023/day/20
"""

HIGH = 1
LOW = 0
assert LOW < HIGH

class OwnedDeque(deque):
    def __init__(self, *args, owner: 'Module', **kwargs):
        self.owner = owner
        super().__init__(*args, **kwargs)


class InputHandler:
    def __init__(self, wrapped_deque: OwnedDeque[tuple[int, int]], key: int):
        self.wrapped_deque = wrapped_deque
        self.key = key

    @property
    def owner(self) -> 'Module':
        return self.wrapped_deque.owner

    def append(self, value):
        self.wrapped_deque.append((self.key, value))


class Module(ABC):
    def __init__(self, id_: str):
        self.id = id_
        self.output_connections: list[Union[InputHandler, OwnedDeque]] = []
        self.low_count = 0
        self.high_count = 0

    @abstractmethod
    def tick(self) -> list['Module']:
        """
        Add signal to input buffers of connected modules as required.
        Return a list of Modules which have been pinged.
        """
        ...

    def send_value(self, value: int) -> list['Module']:
        activated: list[Module] = []
        for output in self.output_connections:
            output.append(value)
            activated.append(output.owner)

            if value == HIGH:
                self.high_count += 1
            else:
                self.low_count += 1
        return activated

    @abstractmethod
    def get_input(self) -> Union[OwnedDeque[int], InputHandler]:
        ...

    def add_output_connection(self, destination: OwnedDeque[int]):
        self.output_connections.append(destination)

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"id={repr(self.id)}, "
                f"ins={len(self.get_input())} "
                f"outs={repr([o.owner.id for o in self.output_connections])}"
                f")")


class Broadcaster(Module):
    def __init__(self, id_: str):
        super().__init__(id_)
        self.input = OwnedDeque(owner=self)

    def tick(self) -> list['Module']:
        if not len(self.input):
            return []

        value = self.input.popleft()
        return self.send_value(value)

    def get_input(self) -> OwnedDeque[int]:
        return self.input


class FlipFlop(Module):
    def __init__(self, id_: str):
        super().__init__(id_)
        self.state = False
        self.input = OwnedDeque(owner=self)

    def get_input(self) -> OwnedDeque[int]:
        return self.input

    def tick(self) -> list['Module']:
        """
        If a flip-flop module receives a low pulse, it flips between on and off.
        If it was off, it turns on and sends a high pulse.
        If it was on, it turns off and sends a low pulse.
        """
        if not len(self.input):
            return []

        value = self.input.popleft()
        previous_state = self.state
        if value == LOW:
            self.state = not self.state

        if self.state != previous_state:
            return self.send_value(HIGH if self.state else LOW)
        else:
            return []


class Conjunction(Module):
    def __init__(self, id_: str):
        super().__init__(id_)
        self.__input: OwnedDeque[tuple[int, int]] = OwnedDeque(owner=self)
        self.input_handlers: list[InputHandler] = []
        self.input_states_memory: list[int] = []

    def get_input(self) -> InputHandler:
        new_handler = InputHandler(self.__input, len(self.input_handlers))
        self.input_handlers.append(new_handler)
        self.input_states_memory.append(LOW)
        return new_handler

    def tick(self) -> list['Module']:
        """
        When a pulse is received, the conjunction module first updates its memory for that input.
        Then, if it remembers high pulses for all inputs, it sends a low pulse;
        otherwise, it sends a high pulse.
        """
        if not len(self.__input):
            return []

        key, value = self.__input.popleft()
        self.input_states_memory[key] = value
        if min(self.input_states_memory) == HIGH:
            value = LOW
        else:
            value = HIGH
        return self.send_value(value)

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"id={repr(self.id)}, "
                f"ins={len(self.__input)} "
                f"outs={repr([o.owner.id for o in self.output_connections])}"
                f")")

class Button(Broadcaster):
    def press(self):
        self.input.append(-1)


def build_network(input_path: str):
    network: dict[str, Module] = {}
    connection_to_add: dict[str, list[str]] = {}
    for line in input_lines(input_path):
        module_type_str, connections_list = line.split(" -> ")
        connections: list[str] = connections_list.split(", ")

        if module_type_str == "broadcaster":
            module_type = Broadcaster
            id_str = "broadcaster"
        else:
            if module_type_str[0] == "%":
                module_type = FlipFlop
            elif module_type_str[0] == "&":
                module_type = Conjunction
            else:
                raise ValueError(f"Unknown module type {module_type_str}")
            id_str = module_type_str[1:]

        network[id_str] = module_type(id_=id_str)
        connection_to_add[id_str] = connections

    network['button'] = Button(id_="button")
    connection_to_add['button'] = ["broadcaster"]

    # Check for any dead end connections
    all_connected_to: set[str] = set()
    for connections in connection_to_add.values():
        for con in connections:
            all_connected_to.add(con)
    for con in all_connected_to:
        if con not in network:
            network[con] = Broadcaster(id_=con)

    # Now make connections
    for module_id, connections in connection_to_add.items():
        module = network[module_id]
        for connection_id in connections:
            to_connect: Module = network[connection_id]
            module.add_output_connection(to_connect.get_input())

    return network


def part_1() -> Union[int, str]:
    network = build_network("input.txt")

    num_button_presses = 1000
    for _ in range(num_button_presses):
        pulse_queue: deque[Module] = deque()

        network['button'].get_input().append(LOW)
        pulse_queue.append(network['button'])

        while len(pulse_queue):
            module: Module = pulse_queue.popleft()
            new = module.tick()
            for n in new:
                pulse_queue.append(n)

    total_highs = sum([m.high_count for m in network.values()])
    total_lows = sum([m.low_count for m in network.values()])

    return total_highs * total_lows


def part_2() -> Union[int, str]:
    network = build_network("input.txt")

    num_button_presses = 1000000
    i = 0
    for i in range(num_button_presses):
        pulse_queue: deque[Module] = deque()

        network['button'].get_input().append(LOW)
        pulse_queue.append(network['button'])

        while len(pulse_queue):
            module: Module = pulse_queue.popleft()
            new = module.tick()
            for n in new:
                pulse_queue.append(n)

        if network['rx'].low_count:
            print(network['rx'].low_count)
            break

    return i


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
