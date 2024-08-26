import re
import time

import pyperclip

from aoc_utils import *


"""
https://adventofcode.com/2015/day/11
"""

class Validator:
    valid: bool

    def feed(self, c: str) -> bool:
        """Returns bool as to whether to continue processing"""
        return True


class ValidatorRun(Validator):
    def __init__(self):
        super().__init__()
        self.valid = False
        self.last_char: int = 0
        self.run_len = 0

    def feed(self, c: str):
        if not self.valid:
            if ord(c) == self.last_char + 1:
                self.run_len +=1
                if self.run_len == 3:
                    self.valid = True
            else:
                self.run_len = 1
            self.last_char = ord(c)
        return True


class ValidatorBadLetters(Validator):
    def __init__(self):
        super().__init__()
        self.valid = True

    def feed(self, c: str) -> bool:
        if c in "iol":
            self.valid = False
            return False
        return True


class ValidatorPairs(Validator):
    def __init__(self):
        super().__init__()
        self.string = ""

    @property
    def valid(self):
        groups = [m.group() for m in re.finditer(r"(.)\1", self.string)]
        return len(groups) >= 2

    def feed(self, c: str) -> bool:
        self.string += c
        return True


def part_1() -> Union[int, str]:
    ord_a = ord("a")
    ord_z = ord("z")

    def increment_word_chars(_chars: list[int]) -> list[int]:
        _chars[-1] += 1

        overflow = True
        pos = -1
        while overflow:
            overflow = False
            if _chars[pos] >= ord_z:
                _chars[pos] = ord_a
                _chars[pos - 1] += 1
                pos -= 1
                overflow = True
        return _chars

    word_chars: list[int] = [ord(c) for c in raw_input(INPUT_PATH).strip()]

    def is_valid(_word_chars: list[int]) -> bool:
        validators: list[Validator] = [ValidatorRun(), ValidatorBadLetters(), ValidatorPairs()]
        for char_int in _word_chars:
            char = chr(char_int)
            for validator in validators:
                if not validator.feed(char):
                    return False
        for validator in validators:
            if not validator.valid:
                return False
        return True

    while not is_valid(word_chars):
        word_chars = increment_word_chars(word_chars)
        #print("".join([chr(wc) for wc in word_chars]))

    return "".join([chr(wc) for wc in word_chars])



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
