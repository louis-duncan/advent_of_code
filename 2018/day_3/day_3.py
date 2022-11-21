from typing import Tuple, Iterable, List


class Claim:
    def __init__(
            self,
            _id: int,
            pos: Tuple[int, int],
            size: Tuple[int, int]
    ):
        self.id = _id
        self.x, self.y = pos
        self.width, self.height = size

    @property
    def pos(self) -> Tuple[int, int]:
        return self.x, self.y

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height

    @property
    def inch_coords(self) -> Iterable[Tuple[int, int]]:
        for dy in range(self.height):
            for dx in range(self.width):
                yield self.x + dx, self.y + dy

    @staticmethod
    def from_str(claim_str: str) -> 'Claim':
        id_str, claim_str = claim_str.split("@")
        pos_str, size_str = claim_str.split(":")

        _id = int(id_str.strip("# "))

        pos_parts = [int(pos_part.strip()) for pos_part in pos_str.split(",")]
        pos = (pos_parts[0], pos_parts[1])

        size_parts = [int(size_part.strip()) for size_part in size_str.split("x")]
        size = (size_parts[0], size_parts[1])

        return Claim(_id, pos, size)

    def __repr__(self):
        return f"#{self.id} @ {self.x},{self.y}: {self.width}x{self.height}"


def main():
    size = 1000
    sheet = [[0] * size for i in range(size)]

    with open("input.txt", "r") as fh:
        claims: List[Claim] = [Claim.from_str(line.strip()) for line in fh.readlines()]

    for claim in claims:
        for pos in claim.inch_coords:
            sheet[pos[0]][pos[1]] += 1

    for claim in claims:
        for pos in claim.inch_coords:
            if sheet[pos[0]][pos[1]] > 1:
                break
        else:
            print(claim)
            break


if __name__ == '__main__':
    main()
