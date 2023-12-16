import re
from typing import List, Dict, Tuple
from functools import cache, cached_property


class Sensor:
    def __init__(self, pos: Tuple[int, int], dist: Tuple[int, int]):
        self.x = pos[0]
        self.y = pos[1]
        self.dist_x = dist[0]
        self.dist_y = dist[1]
        self.dist: int = man_distance(pos, dist)

    @cached_property
    def pos(self) -> Tuple[int, int]:
        return self.x, self.y

    @cached_property
    def y_min(self) -> int:
        return self.y - self.dist

    @cached_property
    def y_max(self) -> int:
        return self.y + self.dist

    @cached_property
    def max_width(self) -> int:
        return (self.dist * 2) + 1

    @cache
    def range_at_y(self, y) -> Tuple[int, int]:
        dy = abs(abs(self.y) - abs(y))
        dx = self.dist - dy
        return self.x - dx, self.x + dx

    def __repr__(self):
        return f"Sensor(pos={self.x},{self.y}, dist={self.dist})"


def man_distance(pos_1: Tuple[int, int], pos_2: Tuple[int, int]) -> int:
    return abs((abs(pos_1[0]) - abs(pos_2[0]))) + abs((abs(pos_1[1]) - abs(pos_2[1])))


def ranges_overlap(range_1: Tuple[int, int], range_2: Tuple[int, int]) -> bool:
    return range_1[0] <= range_2[0] <= range_1[1] or range_2[0] <= range_1[0] <= range_2[1]


def merge_ranges(range_1: Tuple[int, int], range_2: Tuple[int, int]) -> Tuple[int, int]:
    return min(range_1[0], range_2[0]), max(range_1[1], range_2[1])


def num_sensors_and_beacons_in_row(y: int, sensors: List[Sensor]):
    beacons = set([(s.dist_x, s.dist_y) for s in sensors if s.dist_y == y])
    sensors = [s for s in sensors if s.y == y]
    return len(beacons) + len(sensors)


def part_1():
    sensors: List[Sensor] = []
    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            parts = re.findall(r"[x,y]=(-?\d*)", line)
            sensors.append(
                Sensor(
                    (int(parts[0]), int(parts[1])),
                    (int(parts[2]), int(parts[3]))
                )
            )

    qy = 11

    ranges = []

    for s in sensors:
        if s.y_min <= qy <= s.y_max:
            new_range = s.range_at_y(qy)
            for i in range(len(ranges)):
                if ranges_overlap(new_range, ranges[i]):
                    ranges[i] = merge_ranges(new_range, ranges[i])
                    break
            else:
                ranges.append(new_range)

    done_collapsing = False
    while not done_collapsing:
        done_collapsing = True
        for i in range(len(ranges) - 1):
            overlapped = False
            for j in range(i + 1, len(ranges)):
                if ranges_overlap(ranges[i], ranges[j]):
                    ranges[i] = merge_ranges(ranges[i], ranges[j])
                    ranges.pop(j)
                    overlapped = True
                    break
            if overlapped:
                done_collapsing = False
                break

    tot = 0
    for r in ranges:
        tot += (r[1] - r[0]) + 1
    num_beacons = num_sensors_and_beacons_in_row(qy, sensors)
    print(ranges)
    print(tot - num_beacons)


def x_covered(x, ranges: List[Tuple[int, int]]) -> bool:
    for r in ranges:
        if r[0] <= x <= r[1]:
            return True
    return False


def part_2():
    sensors: List[Sensor] = []
    with open("input.txt", "r") as fh:
        for line in fh.readlines():
            parts = re.findall(r"[x,y]=(-?\d*)", line)
            sensors.append(
                Sensor(
                    (int(parts[0]), int(parts[1])),
                    (int(parts[2]), int(parts[3]))
                )
            )

    pos_min = -1
    pos_max = 4000000

    lines_ranges = []

    for y in range(pos_min, pos_max):
        ranges = []
        for s in sensors:
            if s.y_min <= y <= s.y_max:
                new_range = s.range_at_y(y)
                for i in range(len(ranges)):
                    if ranges_overlap(new_range, ranges[i]):
                        ranges[i] = merge_ranges(new_range, ranges[i])
                        break
                else:
                    ranges.append(new_range)

        done_collapsing = False
        while not done_collapsing:
            done_collapsing = True
            for i in range(len(ranges) - 1):
                overlapped = False
                for j in range(i + 1, len(ranges)):
                    if ranges_overlap(ranges[i], ranges[j]):
                        ranges[i] = merge_ranges(ranges[i], ranges[j])
                        ranges.pop(j)
                        overlapped = True
                        break
                if overlapped:
                    done_collapsing = False
                    break

        lines_ranges.append(list(sorted(ranges)))

    pass

    done = False
    for i in range(1, len(lines_ranges) - 1):
        if len(lines_ranges[i]) > 1:
            for r in range(len(lines_ranges[i]) - 1):
                if lines_ranges[i][r][1] == lines_ranges[i][r + 1][0] - 2:
                    x = lines_ranges[i][r][1] + 1
                    if x_covered(x, lines_ranges[i - 1]) and x_covered(x, lines_ranges[i + 1]):
                        print(x, i - 1)
                        done = True
                        break
        if done:
            break


if __name__ == '__main__':
    part_2()
