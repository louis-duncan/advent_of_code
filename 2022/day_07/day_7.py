from typing import List, Optional, Union, Generator, Tuple
from functools import cache, cached_property


class Dir:
    def __init__(self, name: str):
        self.name = name
        self.dirs: List[Dir] = []
        self.files: List[File] = []
        self.parent: Optional[Dir] = None

    def __repr__(self):
        return f"Dir(name={self.name}), n_dirs={len(self.dirs)}, n_files={len(self.files)}"

    @cached_property
    def size(self) -> int:
        tot = 0
        for d in self.dirs:
            tot += d.size
        for f in self.files:
            tot += f.size
        return tot

    def add(self, other: Union['Dir', 'File']):
        if isinstance(other, Dir):
            self.dirs.append(other)
        elif isinstance(other, File):
            self.files.append(other)
        else:
            raise TypeError(f"Cannot add object of type '{other.__class__.__name__}'")
        other.parent = self

    def get_dir(self, dir_name: str) -> Union['Dir', None]:
        for d in self.dirs:
            if d.name == dir_name:
                return d
        return None


class File:
    def __init__(self, name: str, file_size: int):
        self.name = name
        self.size = file_size
        self.parent: Optional[Dir] = None

    def __repr__(self):
        return f"File(name={self.name}, size={self.size})"


def command_parser(lines: List[str]) -> Generator[Tuple[str, List[str]], None, None]:
    current_command = lines[0][2:].strip()
    current_lines = []
    for line in lines[1:]:
        line = line.strip()
        if line.startswith("$"):
            yield current_command, current_lines
            current_command = line[2:]
            current_lines = []
        else:
            current_lines.append(line)
    yield current_command, current_lines


def print_dir(dir_obj: Dir, level=0, pad="  "):
    print(f"{level * pad}{dir_obj.name} - dir - {dir_obj.size}")
    for d in dir_obj.dirs:
        print_dir(d, level=level+1)
    for f in dir_obj.files:
        print(f"{(level + 1) * pad}{f.name} - file - {f.size}")


def size_gen(root_dir: Dir) -> Generator[Tuple[str, int], None, None]:
    yield root_dir.name, root_dir.size
    for d in root_dir.dirs:
        yield from size_gen(d)


def main():
    root_dir = Dir("/")
    cur_dir = root_dir
    with open("input.txt", "r") as fh:
        command_gen = command_parser(fh.readlines())
    _ = command_gen.__next__()

    for command, lines in command_gen:
        match command.split():
            case ["cd", ch_dir_name]:
                if ch_dir_name == "..":
                    cur_dir: Dir = cur_dir.parent
                    if cur_dir is None:
                        raise Exception("We ended up outside the file system...")
                else:
                    if new_dir := cur_dir.get_dir(ch_dir_name):
                        cur_dir = new_dir
                    else:
                        new_dir = Dir(ch_dir_name)
                        cur_dir.add(new_dir)
                        cur_dir = new_dir
            case ["ls"]:
                for line in lines:
                    part_1, part_2 = line.split(" ")
                    if part_1 == "dir":
                        cur_dir.add(Dir(part_2))
                    else:
                        size_str, file_name = part_1, part_2
                        size = int(size_str)
                        cur_dir.add(File(file_name, size))
            case _:
                raise ValueError(f"Unexpected command '{command}'")

    print_dir(root_dir)

    size_needed = 30000000 - (70000000 - root_dir.size)
    dir_sizes = sorted([size for name, size in size_gen(root_dir)])
    for size in dir_sizes:
        if size >= size_needed:
            print(size)
            break


if __name__ == '__main__':
    main()
