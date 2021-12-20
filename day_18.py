from __future__ import annotations

import copy
from typing import Union, Optional, List, Any
from math import ceil, floor, inf

test_data = [
    [[[0, [5, 8]], [[1, 7], [9, 6]]], [[4, [1, 2]], [[1, 4], 2]]],
    [[[5, [2, 8]], 4], [5, [[9, 9], 0]]],
    [6, [[[6, 2], [5, 6]], [[7, 6], [4, 7]]]],
    [[[6, [0, 7]], [0, 9]], [4, [9, [9, 0]]]],
    [[[7, [6, 4]], [3, [1, 3]]], [[[5, 5], 1], 9]],
    [[6, [[7, 3], [3, 2]]], [[[3, 8], [5, 7]], 4]],
    [[[[5, 4], [7, 7]], 8], [[8, 3], 8]],
    [[9, 3], [[9, 9], [6, [4, 9]]]],
    [[2, [[7, 7], 7]], [[5, 8], [[9, 3], [0, 2]]]],
    [[[[5, 2], 5], [8, [3, 7]]], [[5, [7, 5]], [4, 4]]],
]

real_data = [
    [[[0, 6], [[8, 9], [3, 7]]], [[[3, 4], [7, 0]], [[6, 9], [4, 8]]]],
    [[2, 2], [[[7, 7], 5], [[0, 7], 2]]],
    [6, [9, [[7, 9], 7]]],
    [[[[5, 1], [9, 3]], 8], [4, [2, [6, 6]]]],
    [[[4, 3], [0, 4]], [[[4, 5], [9, 3]], 3]],
    [[[[2, 7], 7], [[6, 5], 6]], [[[2, 3], [7, 9]], [0, 3]]],
    [[[3, [6, 2]], [7, [9, 4]]], 3],
    [[[[9, 3], 4], [3, 9]], 8],
    [[[7, 8], [[2, 6], 1]], [[[1, 7], 5], [[5, 6], [6, 1]]]],
    [[[[0, 7], 9], [[6, 6], [8, 4]]], [[[9, 2], [4, 8]], [[8, 5], [0, 6]]]],
    [[6, [[5, 6], [3, 8]]], [[8, 9], [4, 3]]],
    [[[[0, 6], 1], [[2, 4], [1, 4]]], [[7, 5], [8, 3]]],
    [[[[0, 7], 1], [[5, 7], 7]], [[[3, 3], [6, 7]], [[2, 8], [2, 9]]]],
    [[7, 7], [[1, [3, 7]], 9]],
    [[8, [[3, 0], 0]], [[[8, 3], 0], 9]],
    [[[[6, 2], [2, 6]], 3], [6, [[4, 7], 2]]],
    [[[5, [2, 3]], [8, [8, 7]]], [[0, 0], 2]],
    [[1, 6], [7, [7, [9, 0]]]],
    [[[7, [7, 6]], [7, 4]], [[7, 2], [6, 5]]],
    [1, [[8, [9, 5]], 2]],
    [[[[8, 2], [6, 5]], [4, [9, 2]]], [[0, [2, 6]], [6, 6]]],
    [[1, [[7, 2], 5]], [[[6, 0], [8, 1]], 8]],
    [[[[0, 6], [6, 6]], 2], [[4, 2], [2, 4]]],
    [[5, [9, 0]], [2, 5]],
    [7, [[9, 7], [[9, 9], 4]]],
    [[5, [[6, 4], 7]], [8, [[4, 4], [9, 0]]]],
    [2, [[[3, 2], [1, 9]], [[3, 8], [7, 5]]]],
    [[[[8, 2], 0], [5, [4, 3]]], 0],
    [[[0, [7, 8]], [[9, 6], 7]], [[7, [1, 0]], [[0, 3], 7]]],
    [[[[8, 3], 0], [[4, 8], [7, 9]]], [[7, 1], [[8, 4], [4, 4]]]],
    [[[2, 0], [[6, 6], 7]], [[2, [3, 9]], [[5, 6], [4, 6]]]],
    [[[[1, 4], 8], [9, 6]], 8],
    [[7, [9, 1]], [1, [[8, 5], [6, 8]]]],
    [8, [[2, 6], 5]],
    [[[9, [7, 8]], [[7, 8], 6]], 3],
    [1, [[[2, 1], 7], [[2, 6], 7]]],
    [[7, [4, [6, 1]]], [[[4, 9], 8], [[0, 1], [1, 7]]]],
    [[[7, 9], [[2, 6], [2, 4]]], [[2, [1, 7]], [[3, 9], [8, 9]]]],
    [[[[4, 5], [4, 7]], [[4, 0], [9, 9]]], 0],
    [3, [[[6, 9], 2], [5, 3]]],
    [1, [8, [[0, 8], [1, 3]]]],
    [[[7, [9, 2]], [4, [0, 3]]], 2],
    [3, [[[7, 7], 6], [[8, 4], 1]]],
    [[[[6, 3], [2, 6]], [[6, 9], [8, 1]]], [[[2, 1], [7, 5]], [[7, 3], [7, 3]]]],
    [[[1, 6], [[5, 1], [5, 0]]], [[1, 0], [6, 9]]],
    [[[[8, 6], [3, 3]], [[2, 1], [4, 1]]], [1, [[7, 7], [8, 5]]]],
    [[1, 5], [6, [[2, 3], [2, 4]]]],
    [[0, [7, [9, 0]]], [9, 0]],
    [[[5, [1, 9]], [0, [9, 8]]], [[[6, 7], [6, 3]], [8, 1]]],
    [[[4, 7], [6, [2, 1]]], 5],
    [[3, [4, 0]], [2, [4, 5]]],
    [[[4, 0], [6, [8, 3]]], [[0, 6], 8]],
    [[[[9, 9], 0], [[1, 8], 0]], [[1, 6], [3, 4]]],
    [[[[4, 3], 4], 1], [0, [[2, 1], [3, 9]]]],
    [[[8, [6, 2]], [6, 0]], 7],
    [[9, [6, [3, 1]]], [[[5, 9], 0], [4, 5]]],
    [4, [7, [[2, 5], 4]]],
    [[2, [8, [2, 9]]], [[[0, 1], [3, 5]], 1]],
    [[[7, 9], [7, 3]], [[1, [7, 1]], [1, 2]]],
    [[[7, 0], [[1, 0], 8]], [[9, [7, 6]], [9, [7, 2]]]],
    [[[8, 1], [[0, 6], 2]], [9, [[1, 8], [5, 4]]]],
    [6, [[[9, 5], [5, 4]], 3]],
    [[4, [[6, 8], [8, 3]]], [[9, [0, 9]], 7]],
    [[[6, 9], [[2, 3], 8]], [[9, [5, 1]], [[7, 6], 5]]],
    [[0, 1], 5],
    [[4, [1, 9]], [[8, 0], 8]],
    [[5, [0, 6]], [1, 8]],
    [[[[9, 2], 7], 7], [4, [1, [5, 6]]]],
    [[7, [9, [6, 5]]], [[6, 9], 1]],
    [[[5, 2], [0, [1, 4]]], [[0, 4], [[9, 4], 8]]],
    [[[[7, 1], [4, 9]], 3], [[[4, 5], 8], [7, [0, 4]]]],
    [[[9, [8, 0]], 7], [[[4, 5], 8], [[4, 3], [8, 5]]]],
    [[9, [7, 0]], [[3, [1, 7]], [[7, 0], 7]]],
    [[2, [[6, 2], 6]], 8],
    [[[8, [9, 6]], [[5, 8], [7, 2]]], [4, [9, 9]]],
    [[[[0, 5], 0], [[8, 4], 4]], [[7, 9], 8]],
    [[[0, [0, 3]], [0, [8, 8]]], [[[2, 1], 3], 4]],
    [0, [[4, 1], [[9, 9], 2]]],
    [[3, [7, [6, 7]]], [0, 2]],
    [7, 2],
    [0, [3, [[3, 4], [4, 4]]]],
    [[[[0, 1], [5, 9]], [[4, 2], 7]], [5, [1, 8]]],
    [[7, 1], [[1, [9, 9]], [[8, 4], 8]]],
    [[[1, [8, 3]], [[3, 7], 0]], [[2, 0], [[1, 6], [9, 9]]]],
    [[[1, 4], [1, 4]], [[2, [2, 7]], [2, [7, 1]]]],
    [[1, [[6, 8], [8, 6]]], [0, [8, 0]]],
    [1, [[2, 0], 7]],
    [[[[6, 0], 9], [[6, 9], [8, 3]]], [[3, [9, 9]], 6]],
    [[[[9, 8], [2, 8]], [2, 3]], [6, 2]],
    [[[6, [2, 2]], 7], [[3, [7, 8]], 7]],
    [[[5, [3, 7]], 1], [[[4, 0], 3], [5, 4]]],
    [[[7, [4, 3]], [9, [4, 4]]], 7],
    [[2, [[1, 5], 6]], [[2, 3], [[2, 5], [7, 1]]]],
    [[[[3, 9], [1, 9]], 3], [5, [[0, 6], [3, 2]]]],
    [[[3, [7, 5]], [[7, 7], [2, 8]]], [4, [1, [0, 0]]]],
    [[4, [2, [8, 7]]], [[[0, 5], 0], 9]],
    [9, [9, [6, 4]]],
    [[5, [[4, 9], 2]], [9, 9]],
    [[1, [[6, 0], [9, 9]]], [[[8, 4], 1], [[5, 2], [6, 1]]]],
    [[1, [[9, 0], 8]], 6],
]


class SnailNumber:
    def __init__(
            self, parent: Optional[SnailNumber] = None,
            left: Union[int, SnailNumber] = 0,
            right: Union[int, SnailNumber] = 0
    ):
        self.parent: Optional[SnailNumber] = parent
        self.left: Union[int, SnailNumber] = left
        self.right: Union[int, SnailNumber] = right

    @property
    def depth(self):
        if self.parent is None:
            return 0
        else:
            return 1 + self.parent.depth

    def get_first_child_at_depth(self, depth: int) -> Optional[SnailNumber]:
        if self.depth == depth:
            return self
        else:
            if isinstance(self.left, SnailNumber):
                found = self.left.get_first_child_at_depth(depth)
                if found is not None:
                    return found
            if isinstance(self.right, SnailNumber):
                found = self.right.get_first_child_at_depth(depth)
                if found is not None:
                    return found

    def get_first_child_over_size(self, size: int) -> Optional[SnailNumber]:
        if isinstance(self.left, int):
            if self.left >= size:
                return self
        else:
            found = self.left.get_first_child_over_size(size)
            if found is not None:
                return found
        if isinstance(self.right, int):
            if self.right >= size:
                return self
        else:
            found = self.right.get_first_child_over_size(size)
            if found is not None:
                return found

    def add_to_next_left(self, value: int):
        if self is self.parent.right:
            if isinstance(self.parent.left, int):
                self.parent.left += value
            else:
                self.parent.left.get_right_most().right += value
        else:
            subject = self.parent.parent
            found = False
            while subject is not None and not found:
                if isinstance(subject.left, int) or (not subject.left.contains_num(self) and subject.left is not self):
                    found = True
                else:
                    subject = subject.parent
            if found:
                if isinstance(subject.left, int):
                    subject.left += value
                else:
                    subject.left.get_right_most().right += value

    def add_to_next_right(self, value: int):
        if self is self.parent.left:
            if isinstance(self.parent.right, int):
                self.parent.right += value
            else:
                self.parent.right.get_left_most().left += value
        else:
            subject = self.parent.parent
            found = False
            while subject is not None and not found:
                if isinstance(subject.right, int) or (
                        not subject.right.contains_num(self) and subject.right is not self):
                    found = True
                else:
                    subject = subject.parent
            if found:
                if isinstance(subject.right, int):
                    subject.right += value
                else:
                    subject.right.get_left_most().left += value

    def contains_num(self, other: SnailNumber):
        contains = False
        if self.left is other:
            contains = True
        elif isinstance(self.left, SnailNumber):
            if self.left.contains_num(other):
                contains = True
        if self.right is other:
            contains = True
        elif isinstance(self.right, SnailNumber):
            if self.right.contains_num(other):
                contains = True
        return contains

    def get_right_most(self):
        if isinstance(self.right, int):
            return self
        else:
            return self.right.get_right_most()

    def get_left_most(self):
        if isinstance(self.left, int):
            return self
        else:
            return self.left.get_left_most()

    def replace_with_zero(self):
        if self is self.parent.left:
            self.parent.left = 0
        else:
            self.parent.right = 0

    def reduce(self):
        done = False
        while not done:
            done = True
            if (child_at_depth := self.get_first_child_at_depth(4)) is not None:
                done = False
                child_at_depth.add_to_next_left(child_at_depth.left)
                child_at_depth.add_to_next_right(child_at_depth.right)
                child_at_depth.replace_with_zero()
                #print("Explode: ", end="")
            elif (child_too_big := self.get_first_child_over_size(10)) is not None:
                done = False
                if isinstance(child_too_big.left, int) and child_too_big.left >= 10:
                    new = [floor(child_too_big.left / 2), ceil(child_too_big.left / 2)]
                    child_too_big.left = SnailNumber(child_too_big, *new)
                elif isinstance(child_too_big.right, int) and child_too_big.right >= 10:
                    new = [floor(child_too_big.right / 2), ceil(child_too_big.right / 2)]
                    child_too_big.right = SnailNumber(child_too_big, *new)
                #print("Split: ", end="")
            else:
                pass
                #print("Done: ", end="")
            #print(self)

    @property
    def magnitude(self):
        if isinstance(self.left, int):
            left_mag = self.left * 3
        else:
            left_mag = self.left.magnitude * 3
        if isinstance(self.right, int):
            right_mag = self.right * 2
        else:
            right_mag = self.right.magnitude * 2
        return left_mag + right_mag

    def __add__(self, other: SnailNumber):
        new = SnailNumber(left=self, right=other)
        self.parent = new
        other.parent = new
        return new

    def __repr__(self):
        return f"[{self.left}, {self.right}]"

    def get_copy(self):
        return copy.deepcopy(self)


def list_to_snail_number(data: List[Any], parent: Optional[SnailNumber] = None) -> SnailNumber:
    new_snail_number = SnailNumber(parent=parent)
    if isinstance(data[0], int):
        new_left = data[0]
    else:
        new_left = list_to_snail_number(data[0], parent=new_snail_number)
    new_snail_number.left = new_left

    if isinstance(data[1], int):
        new_right = data[1]
    else:
        new_right = list_to_snail_number(data[1], parent=new_snail_number)
    new_snail_number.right = new_right

    return new_snail_number


def str_to_int_list(string: str) -> list:
    return [int(c) for c in string.strip("[]").split(",")]


def main():
    global real_data, test_data
    data = real_data

    snail_numbers = [list_to_snail_number(line) for line in data]

    biggest_pair = []
    biggest_mag = 0

    for sn1 in snail_numbers:
        for sn2 in snail_numbers:
            if sn1 is not sn2:
                tot = sn1.get_copy() + sn2.get_copy()
                tot.reduce()
                if tot.magnitude > biggest_mag:
                    biggest_pair = [sn1, sn2]
                    biggest_mag = tot.magnitude

    print(biggest_pair[0])
    print(biggest_pair[1])
    print(biggest_mag)


if __name__ == '__main__':
    main()
