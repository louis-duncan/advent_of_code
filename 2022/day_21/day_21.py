import re


def main():
    functions = {}
    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            if match := re.findall(r"([a-z]*): ([a-z]*) ([+\-/*]|==) ([a-z]*)", line):
                name, v_1, op, v_2 = match[0]
                exec(
                    f"""def {name}():
    return {v_1}() {op} {v_2}()""", globals()
                )
            elif match := re.findall(r"([a-z]*): ([0-9]*)", line):
                name, v = match[0]
                v = int(v)
                exec(
                    f"""def {name}():
    return {v}""", globals()
                )


def test(x):
    global humn

    def humn():
        return x

    return(root())


if __name__ == '__main__':
    main()

    lower = 0
    upper = 10000000000000
    res = -1

    while res != 0:
        t = (upper + lower) // 2
        res = test(t)
        if res == 0:
            print(t)
        elif res > 0:
            lower = t
        elif res < 0:
            upper = t
