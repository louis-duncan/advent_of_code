
def part_1():
    with open("input.txt", "r") as fh:
        seq = fh.read().strip()

    i = 0
    for i in range(len(seq) - 3):
        s = set(seq[i:i + 4])
        if len(s) == 4:
            break
    print(i + 4)


def part_2():
    with open("input.txt", "r") as fh:
        seq = fh.read().strip()

    i = 0
    for i in range(len(seq) - 13):
        s = set(seq[i:i + 14])
        if len(s) == 14:
            break
    print(i + 14)


if __name__ == '__main__':
    part_2()