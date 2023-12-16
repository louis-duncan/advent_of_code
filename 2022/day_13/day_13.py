import json
from functools import cache
from typing import List, Union
import timeit


class Element:
    def __init__(self, data):
        self.data = convert(data)

    def __eq__(self, other):
        return compare_elements(self.data, other.data) is None

    def __gt__(self, other):
        return compare_elements(self.data, other.data) is False

    def __lt__(self, other):
        return compare_elements(self.data, other.data) is True

    def __repr__(self):
        return json.dumps(self.data)


def convert(data):
    return tuple(convert(x) for x in data) if type(data) is list else data


@cache
def compare_elements(obj_1, obj_2) -> Union[bool, None]:
    """Checks that obj_1 is "less than" obj_2"""
    obj_1_is_int = isinstance(obj_1, int)
    obj_2_is_int = isinstance(obj_2, int)

    if obj_1_is_int and obj_2_is_int:
        if obj_1 == obj_2:
            return None
        else:
            return obj_1 < obj_2

    elif not(obj_1_is_int or obj_2_is_int):
        for a, b in zip(obj_1, obj_2):
            if (res := compare_elements(a, b)) is not None:
                return res
        else:
            if len(obj_1) == len(obj_2):
                return None
            else:
                return len(obj_1) < len(obj_2)

    else:
        if obj_1_is_int:
            return compare_elements((obj_1,), obj_2)
        if obj_2_is_int:
            return compare_elements(obj_1, (obj_2,))


def part_1():
    with open("input.txt", "r") as fh:
        pair_strs = [seg.split("\n") for seg in fh.read().split("\n\n")]
        pairs = [[json.loads(a), json.loads(b)] for a, b in pair_strs]

    tot = 0
    for i, (a, b) in enumerate(pairs):
        res = compare_elements(a, b)
        print(i + 1, res)
        if res:
            tot += i + 1

    print(tot)


def part_2():
    with open("input.txt", "r") as fh:
        values: List[Element] = []
        for line in fh.readlines():
            line = line.strip()
            if len(line) > 0:
                values.append(Element(json.loads(line)))

    values.sort()
    div1_pos = 0
    div2_pos = 0
    for i, v in enumerate(values):
        if v.data in [((2,),), ((6,),)]:
            if v.data == ((2,),):
                div1_pos = i + 1
            if v.data == ((6,),):
                div2_pos = i + 1
            #print(">", i + 1, v)
        #else:
            #print(" ", i + 1, v)
    print(div1_pos * div2_pos)


if __name__ == '__main__':
    print(timeit.timeit(part_2, number=10))
