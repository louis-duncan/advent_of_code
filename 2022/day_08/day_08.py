def part_1():
    with open("input.txt", "r") as fh:
        trees = [[int(t) for t in line.strip()] for line in fh.readlines()]

    visibility = []
    for row in trees:
        visibility.append([False for _ in row])

    # Mark all outer trees as visible.
    for x in range(len(trees[0])):
        visibility[0][x] = True
        visibility[-1][x] = True
    for y in range(len(trees)):
        visibility[y][0] = True
        visibility[y][-1] = True

    # For each column of trees, work down from the top and up from the bottom and mark trees as visible.
    for x in range(len(trees[0])):
        highest = 0
        highest_y = 0
        for y in range(len(trees)):
            if trees[y][x] > highest:
                visibility[y][x] = True
                highest = trees[y][x]
                highest_y = y
            if highest == 9:
                break
        highest = 0
        for y in range(len(trees) - 1, highest_y, -1):
            if trees[y][x] > highest:
                visibility[y][x] = True
                highest = trees[y][x]
            if highest == 9:
                break

    # For each row of trees, work left and right and mark trees as visible.
    for y in range(len(trees)):
        highest = 0
        highest_x = 0
        for x in range(len(trees[0])):
            if trees[y][x] > highest:
                visibility[y][x] = True
                highest = trees[y][x]
                highest_x = x
            if highest == 9:
                break
        highest = 0
        for x in range(len(trees[0]) - 1, highest_x, -1):
            if trees[y][x] > highest:
                visibility[y][x] = True
                highest = trees[y][x]
            if highest == 9:
                break

    print("Num hidden:", sum([sum(row) for row in visibility]))

    return trees, visibility


def part_2():
    with open("input.txt", "r") as fh:
        trees = [[int(t) for t in line.strip()] for line in fh.readlines()]

    best = 0

    for x in range(len(trees[0])):
        for y in range(len(trees)):
            x_left = x
            for x_left in range(x-1, -1, -1):
                if trees[y][x_left] >= trees[y][x]:
                    break
            x_right = x
            for x_right in range(x+1, len(trees[0])):
                if trees[y][x_right] >= trees[y][x]:
                    break
            y_up = y
            for y_up in range(y - 1, -1, -1):
                if trees[y_up][x] >= trees[y][x]:
                    break
            y_down = y
            for y_down in range(y + 1, len(trees)):
                if trees[y_down][x] >= trees[y][x]:
                    break
            score = (x - x_left) * (x_right - x) * (y - y_up) * (y_down - y)
            if score > best:
                best = score

    print(best)


if __name__ == "__main__":
    part_2()
