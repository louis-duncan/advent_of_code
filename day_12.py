from __future__ import annotations

from typing import List, Union, Optional

small_test_data = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

big_test_data = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


data = """CI-hb
IK-lr
vr-tf
lr-end
XP-tf
start-vr
lr-io
hb-qi
end-CI
tf-YK
end-YK
XP-lr
XP-vr
lr-EU
tf-CI
EU-vr
start-tf
YK-hb
YK-vr
start-EU
lr-CI
hb-XP
XP-io
tf-EU"""


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.connections = []

    def add_connection(self, other: Cave):
        if other not in self.connections:
            self.connections.append(other)
        if self not in other.connections:
            other.connections.append(self)

    @property
    def big(self) -> bool:
        return self.name.isupper()

    @property
    def small(self) -> bool:
        return not self.big

    def __repr__(self):
        return f"Cave(name={self.name}, connections={[c.name for c in self.connections]})"


class CaveNetwork:
    def __init__(self):
        self.caves: List[Cave] = []

    def get_cave(self, name: str) -> Union[None, Cave]:
        for c in self.caves:
            if c.name == name:
                return c
        return None

    def has_cave(self, name: str) -> bool:
        c = self.get_cave(name)
        return c is not None

    def __repr__(self):
        return f"CaveNetwork(caves={[c.name for c in self.caves]})"

    def __str__(self):
        return "\n".join([str(c) for c in self.caves])


class Path:
    def __init__(self, route: List[Cave]):
        self.route: List[Cave] = route

    def has_double_small_visit(self) -> bool:
        for cave in self.route:
            if cave.small and self.route.count(cave) == 2:
                return True
        return False

    def available_routes(self) -> List[Path]:
        if self.route[-1].name == "end":
            return [self]
        else:
            possible_steps = []
            for cave in self.route[-1].connections:
                if cave.name == "start":
                    pass
                elif cave not in self.route:
                    possible_steps.append(cave)
                else:
                    if cave.big:
                        possible_steps.append(cave)
                    else:
                        if not self.has_double_small_visit():
                            possible_steps.append(cave)
            new_paths = []
            for p in possible_steps:
                new = self.get_copy()
                new.route.append(p)
                for r in new.available_routes():
                    new_paths.append(r)
            return new_paths

    def get_copy(self):
        return Path(list(self.route))


def load_caves(data_lines: List[str]) -> CaveNetwork:
    caves = CaveNetwork()
    for line in data_lines:
        name, con = line.split("-")

        if (subject_cave := caves.get_cave(name)) is None:
            subject_cave = Cave(name)
            caves.caves.append(subject_cave)

        if (connection_cave := caves.get_cave(con)) is None:
            connection_cave = Cave(con)
            caves.caves.append(connection_cave)

        subject_cave.add_connection(connection_cave)

    return caves


def all_paths(caves: CaveNetwork, path: List[Cave]) -> List[List[Cave]]:
    assert len(path) > 0

    if path[-1].name == "end":
        return [path]

    paths: List[List[Cave]] = []

    for cave in path[-1].connections:
        if cave not in path or cave.big:
            new_path = list(path)
            new_path.append(cave)
            new_paths = all_paths(caves, new_path)
            for p in new_paths:
                paths.append(p)

    return paths


def main():
    global data

    caves = load_caves(data.split("\n"))

    print(caves)
    print()

    base_path = Path([caves.get_cave("start")])

    paths = base_path.available_routes()

    for path in paths:
        print(",".join([c.name for c in path.route]))
    print(len(paths))


if __name__ == '__main__':
    main()
