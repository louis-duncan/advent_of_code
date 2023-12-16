def part_1():
    count = 0
    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            pair_1, pair_2 = line.strip().split(",")
            pair_1 = [int(n) for n in pair_1.split("-")]
            pair_2 = [int(n) for n in pair_2.split("-")]
            if pair_1[0] <= pair_2[0] and pair_1[1] >= pair_2[1]:
                count += 1
            elif pair_2[0] <= pair_1[0] and pair_2[1] >= pair_1[1]:
                count += 1
    print(count)

def part_2():
    count = 0
    areas = {}
    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            pair_1, pair_2 = line.strip().split(",")
            pair_1 = [int(n) for n in pair_1.split("-")]
            pair_2 = [int(n) for n in pair_2.split("-")]

            if pair_1[1] >= pair_2[0] and pair_1[0] <= pair_2[1]:
                count += 1
            elif pair_2[1] >= pair_1[0] and pair_2[0] <= pair_1[1]:
                count += 1
    print(count)
        

if __name__ == "__main__":
    part_2()
