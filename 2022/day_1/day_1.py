from typing import List, Any


class Elf(list):
    def __init__(self):
        super().__init__()
        self.sum: int = 0

    def append(self, __object: int) -> None:
        super(Elf, self).append(__object)
        self.sum += __object

    def pop(self, __index=...) -> Any:
        v = super(Elf, self).pop(__index)
        self.sum -= v
        return v


def load_elves() -> List[Elf]:
    elves = []
    with open("input.txt", "r") as fh:
        new_elf = Elf()
        for line in fh.readlines():
            line = line.strip()
            if line != "":
                new_elf.append(int(line))
            else:
                elves.append(new_elf)
                new_elf = Elf()
        elves.append(new_elf)
    return elves


def main():
    elves = load_elves()
    elves.sort(key=lambda x: x.sum, reverse=True)
    print(elves[0].sum + elves[1].sum + elves[2].sum)


if __name__ == '__main__':
    main()
