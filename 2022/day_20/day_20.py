from typing import List


class Item:
    def __init__(self, value):
        self.value: int = value
        self.next: Item = self
        self.last: Item = self

    def __repr__(self):
        return str(self.value)

    def move_left(self):
        a = self.last.last
        b = self.last
        c = self
        d = self.next

        a.next = c
        c.last = a
        c.next = b
        b.last = c
        b.next = d
        d.last = b

    def move_right(self):
        a = self.last
        b = self
        c = self.next
        d = self.next.next

        a.next = c
        c.last = a
        c.next = b
        b.last = c
        b.next = d
        d.last = b


def iter_items(items):
    item = items[0]
    for item in items:
        if item.value == 0:
            break

    for _ in items:
        yield item
        item = item.next


def shuffle(items):
    for item in items:
        #print(item)
        right = item.value >= 0
        for _ in range(abs(item.value)):
            if right:
                item.move_right()
            else:
                item.move_left()
        #print(", ".join([str(i.value) for i in iter_items(items)]))


def main():
    items: List[Item] = []
    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            items.append(Item(int(line.strip())))
    items[0].last = items[-1]
    items[-1].next = items[0]

    for item in items:
        item.original_value = item.value * 811589153
        item.value = (item.value * 811589153) % (len(items) - 1)

    for i in range(len(items) - 1):
        items[i].next = items[i + 1]
        items[i + 1].last = items[i]

    print(", ".join([str(i.original_value) for i in iter_items(items)]))
    for _ in range(10):
        shuffle(items)
        print(", ".join([str(i.original_value) for i in iter_items(items)]))

    shuffled = list(iter_items(items))

    print(shuffled[1000 % len(shuffled)].original_value)
    print(shuffled[2000 % len(shuffled)].original_value)
    print(shuffled[3000 % len(shuffled)].original_value)
    print(shuffled[1000 % len(shuffled)].original_value +
          shuffled[2000 % len(shuffled)].original_value +
          shuffled[3000 % len(shuffled)].original_value
          )


if __name__ == '__main__':
    main()
