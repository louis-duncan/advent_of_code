from math import copysign
from typing import Tuple, List, Optional


class Probe:
    def __init__(self, vector: Tuple[int, int], pos: Tuple[int, int]):
        self.pos: Tuple[int, int] = pos
        self.vector: Tuple[int, int] = vector
        self.path: List[Tuple[int, int]] = [self.pos]

    def step(self):
        self.pos: Tuple[int, int] = tuple(a+b for a, b in zip(self.pos, self.vector))
        self.path.append(self.pos)
        self.vector = (
                          int(self.vector[0] - copysign(1, self.vector[0]) if self.vector[0] != 0 else 0),
                          int(self.vector[1] - 1)
        )


def display_map(x_range=(20, 30), y_range=(-10, -5), path: Optional[List[Tuple[int, int]]] = None):  # x_range=(14, 50), y_range=(267, 225)
    width = max(x_range) + 1
    height = max(y_range) + 1

    grid = []
    for y in range(height):
        grid.append(["░" for _ in range(width)])

    grid[0][0] = "S"

    for y in range(*reversed(y_range)):
        for x in range(*x_range):
            grid[y+1][x+1] = "▒"

    if path is not None:
        for p in path:
            if 0 <= p[0] <= width-1 and 0 <= -p[1] <= height-1:
                grid[-p[1]][p[0]] = "█"

    output = "\n".join(["".join(line) for line in grid])
    print(output)


def test_velocities():
    target = (-10, -5) # (-267, -225)

    highest = Probe((0, 0), (0, 0))
    for i in range(0, 1000):
        probe = Probe(vector=(6, i), pos=(0, 0))
        worked = False
        while probe.pos[1] > target[0]:
            probe.step()
            if target[0] <= probe.pos[1] <= target[1]:
                worked = True
                break
        if worked:
            highest = probe

    display_map(path=highest.path)
    print("Start:", highest.path[0], "Steps:", len(highest.path), "Velocity:", highest.vector)
    print("Max Height:", max([p[1] for p in highest.path]))


def test_velocity(velocity: Tuple[int, int]) -> bool:
    target_depth = (-267, -225)
    target_width = (14, 50)

    probe = Probe(vector=velocity, pos=(0, 0))
    worked = False
    while probe.pos[1] > target_depth[0]:
        probe.step()
        if target_depth[0] <= probe.pos[1] <= target_depth[1] and target_width[0] <= probe.pos[0] <= target_width[1]:
            worked = True
            break
    return worked


def test_x(x: int) -> bool:
    target_width = (14, 50)
    pos = 0
    while x > 0:
        pos += x
        x -= 1
    print("Resting pos:", pos)
    return target_width[0] <= pos <= target_width[1]


def main():
    velocities = []
    for y in range(-600, 600):
        for x in range(0, 52):
            if test_velocity((x, y)):
                velocities.append((x, y))
    print(velocities)
    print(len(velocities))


if __name__ == '__main__':
    #test_velocities()
    main()
    pass
