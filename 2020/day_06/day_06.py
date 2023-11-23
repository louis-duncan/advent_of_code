from pathlib import Path


def raw_input(input_path: Path = Path("input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read()
    return data.strip()


def groups(raw_lines: list[str]):
    group_lines = []
    for line in raw_lines:
        if line.strip() != "":
            group_lines.append(line)
        else:
            yield group_lines
            group_lines = []

    if group_lines:
        yield group_lines


def main():
    total = 0

    for group in groups(raw_input().split("\n")):
        group_set = set(group[0])
        for person in group[1:]:
            group_set = group_set.intersection(set(person.strip()))
        total += len(group_set)

    print(total)


if __name__ == "__main__":
    main()
