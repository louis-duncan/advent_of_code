from typing import Tuple, List, Dict, Optional, Union

import numpy as np

small_test_data = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""

test_data = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""

real_data = """"""


class Region:
    def __init__(
            self,
            start: Tuple[int, int, int],
            end: Tuple[int, int, int],
            age: Union[int, float] = 0

    ):
        self.x_min: int = min(start[0], end[0])
        self.x_max: int = max(start[0], end[0])
        self.y_min: int = min(start[1], end[1])
        self.y_max: int = max(start[1], end[1])
        self.z_min: int = min(start[2], end[2])
        self.z_max: int = max(start[2], end[2])

        self.age = age

        self.exclusions: List[Region] = []
        self.inclusions: List[Region] = []

    @property
    def start(self):
        return self.x_min, self.y_min, self.z_min

    @property
    def end(self):
        return self.x_max, self.y_max, self.z_max

    @property
    def sum(self):
        self_sum = abs((self.x_max + 1) - self.x_min) * \
                   abs((self.y_max + 1) - self.y_min) * \
                   abs((self.z_max + 1) - self.z_min)
        self_sum -= sum([e.sum for e in self.exclusions])
        self_sum += sum([i.sum for i in self.inclusions])
        return max(0, self_sum)

    def __repr__(self):
        return f"Region(start={self.start}, end={self.end})"


class Reactor:
    def __init__(self):
        self.active_cubes: Dict[Tuple[int, int, int]: bool] = {}

    def set_cube(self, state: bool, xyz: Tuple[int, int, int]):
        if state:
            self.active_cubes[xyz] = state
        else:
            try:
                self.active_cubes.pop(xyz)
            except KeyError:
                pass

    def set_range(
            self,
            state: bool,
            start_xyz: Tuple[int, int, int],
            end_xyz: Tuple[int, int, int]
    ):
        count = 0
        x_range = sorted([start_xyz[0], end_xyz[0]])
        for x in range(x_range[0], x_range[1] + 1):
            y_range = sorted([start_xyz[1], end_xyz[1]])
            for y in range(y_range[0], y_range[1] + 1):
                z_range = sorted([start_xyz[2], end_xyz[2]])
                for z in range(z_range[0], z_range[1] + 1):
                    self.set_cube(state, (x, y, z))
                    count += 1
        return count


def get_intersection(region_1: Region, region_2: Region) -> Optional[Region]:
    # Check that there is an intersection
    if region_1.x_min > region_2.x_max or \
            region_2.x_min > region_1.x_max or \
            region_1.y_min > region_2.y_max or \
            region_2.y_min > region_1.y_max or \
            region_1.z_min > region_2.z_max or \
            region_2.z_min > region_1.z_max:
        return None

    start_x = max(region_1.x_min, region_2.x_min)
    end_x = min(region_1.x_max, region_2.x_max)

    start_y = max(region_1.y_min, region_2.y_min)
    end_y = min(region_1.y_max, region_2.y_max)

    start_z = max(region_1.z_min, region_2.z_min)
    end_z = min(region_1.z_max, region_2.z_max)

    new_region = Region(
        (start_x, start_y, start_z),
        (end_x, end_y, end_z),
        min(region_1.age, region_2.age) + round(abs(region_1.age - region_2.age) * 0.75, 6)
    )
    # Check that the region has an area.
    if new_region.sum == 0:
        return None
    else:
        return new_region


def decode_instruction(text: str) -> Tuple[bool, Tuple[int, int, int], Tuple[int, int, int]]:
    state_str, coord_parts_str = text.split(" ")
    state: bool = state_str == "on"
    coord_parts_strs = coord_parts_str.split(",")

    x_bits = [int(c) for c in coord_parts_strs[0].split("=")[1].split("..")]
    y_bits = [int(c) for c in coord_parts_strs[1].split("=")[1].split("..")]
    z_bits = [int(c) for c in coord_parts_strs[2].split("=")[1].split("..")]

    xyz_start: Tuple[int, int, int] = (x_bits[0], y_bits[0], z_bits[0])
    xyz_end: Tuple[int, int, int] = (x_bits[1], y_bits[1], z_bits[1])

    return state, xyz_start, xyz_end


def decode_instructions(text: str) -> List[Tuple[int, bool, Tuple[int, int, int], Tuple[int, int, int]]]:
    instructions: List[Tuple[int, bool, Tuple[int, int, int], Tuple[int, int, int]]] = []
    for i, line in enumerate(text.split("\n")):
        new_base_inst: Tuple[bool, Tuple[int, int, int], Tuple[int, int, int]] = decode_instruction(line)
        new_inst: Tuple[int, bool, Tuple[int, int, int], Tuple[int, int, int]] = (i, ) + new_base_inst
        instructions.append(new_inst)
    return instructions


def main():
    global real_data, test_data, small_test_data

    data = test_data

    instructions = decode_instructions(data)

    on_regions: List[Region] = []
    off_regions: List[Region] = []

    bounding_box = Region((-50, -50, -50), (50, 50, 50))

    for age, state, start, end in instructions:
        if (new_region := get_intersection(Region(start, end), bounding_box)) is not None:
            new_region.age = age
            if state:
                on_regions.append(new_region)
            else:
                off_regions.append(new_region)

    for on_region in on_regions:
        for off_region in off_regions:
            if off_region.age > on_region.age:
                if (overlap := get_intersection(on_region, off_region)) is not None:
                    on_region.exclusions.append(overlap)

    for i in range(len(on_regions) - 1):
        for j in range(i + 1, len(on_regions)):
            assert on_regions[i] is not on_regions[j]
            if (overlap := get_intersection(on_regions[i], on_regions[j])) is not None:
                # Update the overlap with exclusions from the j region.
                for existing_exclusion in on_regions[j].exclusions:
                    if get_intersection(overlap, existing_exclusion) is not None:
                        overlap.exclusions.append(existing_exclusion)
                if overlap.sum > 0:  # There is still some overlap with the i region.
                    # Exclude the whole overlap to prevent double counting, then create new inclusions to represent any
                    # part of the overlap which is in an excluded region of the i region.
                    on_regions[j].exclusions.append(overlap)
                    for existing_exclusion in on_regions[i].exclusions:
                        if (existing_exclusion.age < overlap.age) and \
                                ((protrusion := get_intersection(existing_exclusion, overlap)) is not None):
                            protrusion.age = on_regions[j].age
                            on_regions[j].inclusions.append(protrusion)

    print(sum([r.sum for r in on_regions]))
    return on_regions, off_regions


if __name__ == '__main__':
    #get_intersection(Region((0, 0, 0), (2, 2, 2)), Region((1, 1, 1), (3, 3, 3)))
    r_on, r_off = main()
    pass
