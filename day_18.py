from __future__ import annotations
from typing import Union, Optional, List, Any
from math import ceil, floor

test_data = [[[[4,3],4],4],[7,[[8,4],9]]]


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
                if isinstance(subject.right, int) or (not subject.right.contains_num(self) and subject.right is not self):
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
                print("Explode: ", end="")
            elif (child_too_big := self.get_first_child_over_size(10)) is not None:
                done = False
                if isinstance(child_too_big.left, int) and child_too_big.left >= 10:
                    new = [floor(child_too_big.left / 2), ceil(child_too_big.left / 2)]
                    child_too_big.left = SnailNumber(child_too_big, *new)
                elif isinstance(child_too_big.right, int) and child_too_big.right >= 10:
                    new = [floor(child_too_big.right / 2), ceil(child_too_big.right / 2)]
                    child_too_big.right = SnailNumber(child_too_big, *new)
                print("Split: ", end="")
            else:
                print("Done: ", end="")
            print(self)

    def __add__(self, other: SnailNumber):
        new = SnailNumber(left=self, right=other)
        self.parent = new
        other.parent = new
        return new

    def __repr__(self):
        return f"[{self.left}, {self.right}]"


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


def main():
    global test_data
    data = test_data

    snail_number = list_to_snail_number(data=data)
    small = list_to_snail_number([1, 1])
    print(snail_number)
    print(snail_number + small)
    snail_number.reduce()


if __name__ == '__main__':
    main()
