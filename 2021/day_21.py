import itertools
from typing import Dict, Tuple
from functools import cache

class DeterministicDice:
    def __init__(self):
        self._next = 1
        self.rolls = 0

    def roll(self):
        next_roll = self._next
        self._next += 1
        if self._next > 100:
            self._next = 1
        self.rolls += 1
        return next_roll


def at_least_one_active_state(states: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int]) -> int:
    for value in states.values():
        if value > 0:
            return True
    return False


@cache
def new_place_and_score(pos, score, roll):
    pos = (((pos - 1) + roll) % 10) + 1
    score = score + pos
    return pos, score


def part_two():
    print("Generating states...")

    states = {}
    for player_1_pos in range(1, 11):
        for player_1_score in range(0, 30):
            for player_2_pos in range(1, 11):
                for player_2_score in range(0, 30):
                    for t in [0, 1]:
                        states[((player_1_pos, player_1_score), (player_2_pos, player_2_score), t)] = 0
    states[((10, 0), (6, 0), 0)] = 1

    print("Done.")

    win_score = 21
    player_wins = [0, 0]
    possible_rolls = []  # sum(roll) for roll in itertools.combinations_with_replacement([1, 2, 3], 3)]
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                possible_rolls.append(sum((a, b, c)))
    print(len(possible_rolls))
    while at_least_one_active_state(states):
        for state_turn, count in states.items():
            *state, turn = state_turn
            if count > 0:
                states[state_turn] = 0
                for roll in possible_rolls:
                    new_player_state = new_place_and_score(*state[turn], roll)
                    if new_player_state[1] >= win_score:
                        player_wins[turn] += count
                    else:
                        if turn:  # Was player 2's turn
                            new_state = (state[0], new_player_state, int(not turn))
                        else:  # Was player 1's turn
                            new_state = (new_player_state, state[1], int(not turn))
                        states[new_state] += count
    return player_wins


def main():
    player_positions = [10, 6]
    player_scores = [0, 0]

    dice = DeterministicDice()

    whose_turn = 0
    while max(player_scores) < 21:
        roll = sum([dice.roll() for _ in range(3)])

        player_positions[whose_turn] += roll
        while player_positions[whose_turn] > 10:
            player_positions[whose_turn] -= 10

        player_scores[whose_turn] += player_positions[whose_turn]

        #print(f"Player {whose_turn + 1} rolled {roll}, moved to {player_scores[whose_turn]}, now at score {player_scores[whose_turn]}")
        whose_turn = int(not whose_turn)

    print(player_scores)
    print(dice.rolls)
    print(f"{dice.rolls*min(player_scores)=}")


if __name__ == '__main__':
    p1, p2 = part_two()
    print(f"{p1}, {p2}")
    print(f"{round(p1 / 444356092776315)}, {round(p2 / 341960390180808)}")
    print("Looking for 444356092776315 and 341960390180808")
    print(max(p1, p2))
