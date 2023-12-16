from __future__ import annotations
from typing import List, Callable, Dict, Optional, Union


class Monkey:
    monkeys: List[Monkey] = []

    def __init__(
            self,
            _id: int,
            operation: Callable[[int], int],
            test: Callable[[int], int],
            div: int,
            items: Optional[List[Item]] = None
    ):
        self.monkeys.append(self)
        self.id = _id
        self.operation = operation
        self.div = div
        self.test = test
        if items:
            self.items = items
        else:
            self.items: List[Item] = []
        self.inspect_count = 0

    def __del__(self):
        self.monkeys.remove(self)

    def __repr__(self):
        return f"Monkey(id={self.id}, inspect_count={self.inspect_count}, items={repr(self.items)})"

    def inspect_all_items(self):
        for i in range(len(self.items)):
            self.inspect_item(self.items.pop(0))

    def inspect_item(self, item: Item):
        item.worry_level = self.operation(item.worry_level)
        self.inspect_count += 1
        item.worry_level = item.worry_level % 9699690
        self.throw_item(item)

    def throw_item(self, item: Item):
        next_monkey_id: int = self.test(item.worry_level)
        self.monkeys[next_monkey_id].items.append(item)


class Item:
    def __init__(self, worry_level: int):
        self.worry_level = worry_level

    def __repr__(self):
        return f"{self.worry_level}"


monkey_functions = [
    {  # 0
        'op': lambda old: old * 7,
        'div': 3,
        'test': lambda old: 3 if old % 3 == 0 else 7,
        'min': lambda old: old // 3
    },
    {  # 1
        'op': lambda old: old + 5,
        'div': 11,
        'test': lambda old: 6 if old % 11 == 0 else 4,
        'min': lambda old: old // 11
    },
    {  # 2
        'op': lambda old: old * old,
        'div': 7,
        'test': lambda old: 0 if old % 7 == 0 else 7,
        'min': lambda old: old // 7
    },
    {  # 3
        'op': lambda old: old + 4,
        'div': 2,
        'test': lambda old: 5 if old % 2 == 0 else 1,
        'min': lambda old: old // 2
    },
    {  # 4
        'op': lambda old: old * 17,
        'div': 19,
        'test': lambda old: 2 if old % 19 == 0 else 6,
        'min': lambda old: old // 19
    },
    {  # 5
        'op': lambda old: old + 7,
        'div': 5,
        'test': lambda old: 1 if old % 5 == 0 else 4,
        'min': lambda old: old // 5
    },
    {  # 6
        'op': lambda old: old + 6,
        'div': 17,
        'test': lambda old: 2 if old % 17 == 0 else 0,
        'min': lambda old: old // 17
    },
    {  # 7
        'op': lambda old: old + 3,
        'div': 13,
        'test': lambda old: 3 if old % 13 == 0 else 5,
        'min': lambda old: old // 13
    }
]

test_monkey_functions = [
    {
        'op': lambda old: old * 19,
        'test': lambda old: 2 if old % 23 == 0 else 3
    },
    {
        'op': lambda old: old + 6,
        'test': lambda old: 2 if old % 19 == 0 else 0
    },
    {
        'op': lambda old: old * old,
        'test': lambda old: 1 if old % 13 == 0 else 3
    },
    {
        'op': lambda old: old + 3,
        'test': lambda old: 0 if old % 17 == 0 else 1
    }
]


def load_items(line: str) -> List[Item]:
    nums = [int(n) for n in line.strip().split(", ")]
    return [Item(n) for n in nums]


def load_monkeys(file_name: str, functions: List[Dict[str, Union[Callable[[int], int], int]]]) -> List[Monkey]:
    with open(file_name, "r") as fh:
        monkeys: List[Monkey] = []
        for i, line in enumerate(fh.readlines()):
            monkeys.append(
                Monkey(
                    _id=i,
                    operation=functions[i]['op'],
                    test=functions[i]['test'],
                    items=load_items(line),
                    div=functions[i]['div']
                )
            )
    return monkeys


def main():
    monkeys = load_monkeys("input.txt", monkey_functions)

    for i in range(10000):
        for monkey in monkeys:
            monkey.inspect_all_items()
        if i % 100 == 0:
            print(i)

    for monkey in monkeys:
        print(monkey)

    inspection_counts = list(reversed(sorted([m.inspect_count for m in monkeys])))
    print(inspection_counts)
    print(inspection_counts[0] * inspection_counts[1])


if __name__ == '__main__':
    main()
