from typing import Dict, List, Tuple


def pop_next_step(steps: Dict[str, List[str]]) -> str:
    available_steps: List[str] = []
    for s in steps:
        if len(steps[s]) == 0:
            available_steps.append(s)
    available_steps.sort()
    next_step = available_steps[0]
    steps.pop(next_step)

    for s in steps:
        try:
            steps[s].remove(next_step)
        except ValueError:
            pass

    return next_step


def remove_done_step(steps: Dict[str, List[str]], letter: str):
    steps.pop(letter)
    for s in steps:
        try:
            steps[s].remove(letter)
        except ValueError:
            pass


def list_next_simultaneous_step(steps: Dict[str, List[str]]) -> List[str]:
    available_steps: List[str] = []
    for s in steps:
        if len(steps[s]) == 0:
            available_steps.append(s)
    available_steps.sort()

    return available_steps


def part_1():
    steps: Dict[str, List[str]] = {}  # X: [Y, Z, ...]  "X requires Y, Z, ..."
    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            parts = line.split()
            letter_1, letter_2 = parts[1], parts[7]

            if letter_1 not in steps:
                steps[letter_1] = []
            if letter_2 not in steps:
                steps[letter_2] = []

            steps[letter_2].append(letter_1)

    steps_order = ""
    while len(steps) > 0:
        next_steps = pop_next_step(steps)
        steps_order += "".join(next_steps)
    print(steps_order)


def part_2():
    steps: Dict[str, List[str]] = {}  # X: [Y, Z, ...]  "X requires Y, Z, ..."
    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            parts = line.split()
            letter_1, letter_2 = parts[1], parts[7]

            if letter_1 not in steps:
                steps[letter_1] = []
            if letter_2 not in steps:
                steps[letter_2] = []

            steps[letter_2].append(letter_1)

    cur_time = 0
    num_workers = 5
    job_time = 60
    completion_order = ""
    worker_allocations: List[Tuple[str, int]] = []  # [[step, end time], ...]

    while len(steps) > 0 or len(worker_allocations) > 0:
        # Get next ending time of jobs currently being worked on and set cur_time to that time.
        if len(worker_allocations) > 0:
            cur_time: int = min(worker_allocations, key=lambda x: x[1])[1]

        # Complete any steps which have finished by cur_time.
        done_jobs = []
        for job in worker_allocations:
            if job[1] <= cur_time:
                done_jobs.append(job)
        for job in done_jobs:
            remove_done_step(steps, job[0])
            completion_order += job[0]
            worker_allocations.remove(job)

        # Get any available steps and assign steps to available workers.
        for letter in list_next_simultaneous_step(steps):
            if len(worker_allocations) < num_workers:
                if letter not in (j[0] for j in worker_allocations):
                    end_time = cur_time + job_time + ord(letter) - 64
                    worker_allocations.append((letter, end_time))
            else:
                break

    print(completion_order)
    print(cur_time)


if __name__ == '__main__':
    part_2()
