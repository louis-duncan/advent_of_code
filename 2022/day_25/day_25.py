BASE = 5

def to_decimal(num_str: str) -> int:
    res = 0
    for i, c in enumerate(reversed(num_str)):
        if c == "-":
            c = "-1"
        elif c == "=":
            c = "-2"
        res += int(c) * (BASE ** i)
    return res


def to_snafu(num: int) -> str:
    digits = []
    power = 0
    while BASE ** power < num:
        power += 1

    for p in range(power, -1, -1):
        dig = num // (BASE ** p)
        digits.append(dig)
        num -= dig * (BASE ** p)

    for i in range(len(digits) - 1, -1, -1):
        if digits[i] > 2:
            digits[i] -= 5
            digits[i - 1] += 1
        elif digits[i] < -2:
            digits[i] += 5
            digits[i - 1] -= 1

    output = ""
    for d in digits:
        if d == -1:
            output += "-"
        elif d == -2:
            output += "="
        else:
            output += str(d)

    return output.lstrip("0")


def main():
    tot = 0
    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            tot += to_decimal(line.strip())
    print(to_snafu(tot))


if __name__ == '__main__':
    main()
