def main():
    trees = []
    with open("input.txt", "r") as fh:
        for line in fh:
            trees.append(line.strip())

    x_pos = 0
    y_pos = 0
    height = len(trees)
    width = len(trees[0])

    steps = [
        [1, 1],
        [3, 1],
        [5, 1],
        [7, 1],
        [1, 2]
    ]

    counts = []
    for x_step, y_step in steps:
        count = 0
        x_pos = 0
        y_pos = 0
        while y_pos < height:
            if trees[y_pos][x_pos % width] == "#":
                count += 1

            x_pos += x_step
            y_pos += y_step
        counts.append(count)

    final = counts[0]
    for c in counts[1:]:
        final *= c
    print(final)


if __name__ == '__main__':
    main()
