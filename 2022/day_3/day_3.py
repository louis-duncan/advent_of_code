PRIORITIES = {l: i+1 for i, l in enumerate("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")}


def part_1():
    tot = 0
    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            half_1 = set(line[:len(line) // 2])
            half_2 = set(line[len(line) // 2:])
            tot += PRIORITIES[half_1.intersection(half_2).pop()]
    print(tot)


def part_2():
    tot = 0
    with open("input.txt", "r") as fh:
        count = 0
        base_set = set(PRIORITIES.keys())
        for line in fh.readlines():
            base_set = base_set.intersection(set(line.strip()))
            count += 1
            if count == 3:
                tot += PRIORITIES[base_set.pop()]
                base_set = set(PRIORITIES.keys())
                count = 0

    print(tot)


if __name__ == '__main__':
    part_2()
