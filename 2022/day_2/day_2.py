from functools import cache

ROCK = 1
PAPER = 2
SCISSOR = 3
action_map = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSOR
}
WIN = 6
LOSE = 0
DRAW = 3


@cache
def get_action(them, me):
    if me == "X":  # LOSE
        if them == ROCK:
            return SCISSOR
        elif them == PAPER:
            return ROCK
        else:
            return PAPER
    elif me == "Y":  # DRAW
        if them == ROCK:
            return ROCK
        elif them == PAPER:
            return PAPER
        else:
            return SCISSOR
    elif me == "Z":  # WIN
        if them == ROCK:
            return PAPER
        elif them == PAPER:
            return SCISSOR
        else:
            return ROCK


def main():
    with open("input.txt", "r") as fh:
        actions = [line.strip().split() for line in fh.readlines()]

    score = 0
    for them, me in actions:
        them = action_map[them]
        me = get_action(them, me)
        outcome = DRAW
        if them == ROCK and me == PAPER:
            outcome = WIN
        elif them == ROCK and me == SCISSOR:
            outcome = LOSE
        elif them == PAPER and me == SCISSOR:
            outcome = WIN
        elif them == PAPER and me == ROCK:
            outcome = LOSE
        elif them == SCISSOR and me == ROCK:
            outcome = WIN
        elif them == SCISSOR and me == PAPER:
            outcome = LOSE
        score += me + outcome

    print(score)


if __name__ == '__main__':
    main()
