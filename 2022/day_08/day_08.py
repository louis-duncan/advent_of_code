timings = {
    "noop": 1,
    "addx": 2,
}


def main():
    with open("input.txt", "r") as fh:
        instructions = [
            line.strip().split() for line in fh.readlines()
        ]
    cycle_num = 0
    x = 1
    for i in instructions:
        t = timings[i[0]]
        for _ in range(t):
            if x - 1 <= cycle_num % 40 <= x + 1:
                print("#", end="", flush=True)
            else:
                print(" ", end="", flush=True)
            cycle_num += 1
            if cycle_num % 40 == 0:
                print(flush=True)
        match i:
            case ["addx", n]:
                x += int(n)


if __name__ == '__main__':
    main()
