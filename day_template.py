from pathlib import Path


def raw_input(input_path: Path = Path("input.txt")) -> str:
    with open(input_path, "r") as fh:
        data = fh.read()
    return data


def main():
    ...


if __name__ == "__main__":
    main()
