import datetime
import re
from typing import List, Tuple, Optional

SLEEP = -1
AWAKE = -2


class Sleep:
    def __init__(
            self,
            start: datetime.datetime,
            end: datetime.datetime
    ):
        self.start = start
        self.end = end

    @property
    def minutes(self) -> int:
        d = self.end - self.start
        return int(d.seconds / 60)

    def minute_in_sleep(self, when: int) -> bool:
        return self.start.minute <= when < self.end.minute


class Shift:
    def __init__(self, _date: datetime.datetime):
        self.date = _date
        self.sleeps: List[Sleep] = []

    @property
    def total_sleep_time(self) -> int:
        return sum(sleep.minutes for sleep in self.sleeps)

    def was_asleep_at_minute(self, when: int) -> bool:
        for sleep in self.sleeps:
            if sleep.minute_in_sleep(when):
                return True
        return False


class Guard:
    def __init__(
            self,
            _id: int
    ):
        self.id = _id
        self.shifts: List[Shift] = []

    def __repr__(self):
        return f"Guard(id={self.id})"

    @property
    def total_sleep_time(self):
        return sum([s.total_sleep_time for s in self.shifts])

    def was_asleep_at_minute(self, when: int) -> int:
        """Number of shifts where they were asleep at given minute"""
        count = 0
        for shift in self.shifts:
            if shift.was_asleep_at_minute(when):
                count += 1
        return count


class GuardList(list):
    def get_guard(self, _id) -> Optional[Guard]:
        for g in self:
            if g.id == _id:
                return g
        return None


def main():
    with open("input.txt", "r") as fh:
        input_lines = [line.strip() for line in fh.readlines()]

    formatted = []
    for line in input_lines:
        date_str = line[:18]
        action_str = line[19:]
        date = datetime.datetime.strptime(date_str, "[%Y-%m-%d %H:%M]")

        if action_str == "falls asleep":
            action = SLEEP
        elif action_str == "wakes up":
            action = AWAKE
        else:
            m = re.search(r"\d+", action_str)
            action = int(action_str[m.start(): m.end()])

        formatted.append((date, action))

    formatted.sort(key=lambda x: x[0])

    print(len(formatted))

    guards = GuardList()

    # Get build guards
    shift_start: Optional[datetime.datetime] = None
    sleep_start: Optional[datetime.datetime] = None
    cur_guard: Optional[Guard] = None
    sleeps: List[Sleep] = []
    for entry in formatted:
        if entry[1] == SLEEP:
            sleep_start = entry[0]
        elif entry[1] == AWAKE:
            sleeps.append(Sleep(sleep_start, entry[0]))
        else:
            if cur_guard is not None:
                new_shift = Shift(shift_start)
                for s in sleeps:
                    new_shift.sleeps.append(s)
                cur_guard.shifts.append(new_shift)

            if guards.get_guard(entry[1]) is None:
                guards.append(Guard(entry[1]))

            cur_guard = guards.get_guard(entry[1])
            shift_start = entry[0]
            sleeps = []
    new_shift = Shift(shift_start)
    for s in sleeps:
        new_shift.sleeps.append(s)
    cur_guard.shifts.append(new_shift)

    worst_count = 0
    worst_minute = 0
    worst_guard = None
    for guard in guards:
        minute_counts = [guard.was_asleep_at_minute(m) for m in range(60)]
        if max(minute_counts) > worst_count:
            worst_count = max(minute_counts)
            worst_minute = minute_counts.index(max(minute_counts))
            worst_guard = guard
    print(worst_guard, "Worst Minute:", worst_minute, worst_guard.id * worst_minute)


if __name__ == '__main__':
    main()
