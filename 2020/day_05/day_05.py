from pathlib import Path
from math import ceil, floor


def raw_input(input_path: Path = Path("input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read()
    return data.strip()


def get_location_int(location: str) -> int:
    v = 0
    for i, c in enumerate(reversed(location)):
        v += (2 ** i) * (c == "B" or c == "R")
    return v


def main():
    lowest = 1000
    highest = 0
    seat_ids: set[int] = set()
    for location in raw_input().split("\n"):
        row = get_location_int(location[:7])
        col = get_location_int(location[7:])
        seat_id = (row * 8) + col
        seat_ids.add(seat_id)
        highest = max(seat_id, highest)
        lowest = min(seat_id, lowest)
        if seat_id == 0:
            pass

    for i in range(lowest + 1, highest):
        if i not in seat_ids:
            print(i)
            break

if __name__ == "__main__":
    main()
