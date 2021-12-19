
class FishGroup:
    def __init__(self, num_fish, count_down):
        self.num_fish = num_fish
        self.count_down = count_down

    def __repr__(self):
        return f"FishGroup(num_fish={self.num_fish}, count_down={self.count_down})"


def simplify_fish_list(fish_list):
    group_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for f in fish_list:
        if isinstance(f, int):
            group_counts[f] += 1
        elif isinstance(f, FishGroup):
            group_counts[f.count_down] += f.num_fish

    groups = []
    for i, gc in enumerate(group_counts):
        if gc > 0:
            groups.append(FishGroup(gc, i))

    return groups


def main():
    fish_list = [
        5, 1, 1, 1, 3, 5, 1, 1, 1, 1, 5, 3, 1, 1, 3, 1, 1, 1, 4, 1, 1, 1, 1, 1, 2, 4, 3, 4, 1, 5, 3, 4, 1, 1, 5, 1,
        2, 1, 1, 2, 1, 1, 2, 1, 1, 4, 2, 3, 2, 1, 4, 1, 1, 4, 2, 1, 4, 5, 5, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 5, 5,
        1, 1, 4, 4, 5, 1, 1, 1, 3, 1, 5, 1, 2, 1, 5, 1, 4, 1, 3, 2, 4, 2, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 3,
        5, 4, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 5, 1, 1, 1, 4, 1, 4, 1, 1, 1, 1, 1, 2, 1, 1, 5, 1, 2, 1, 1, 2, 1, 1,
        2, 4, 1, 1, 5, 1, 3, 4, 1, 2, 4, 1, 1, 1, 1, 1, 4, 1, 1, 4, 2, 2, 1, 5, 1, 4, 1, 1, 5, 1, 1, 5, 5, 1, 1, 1,
        1, 1, 5, 2, 1, 3, 3, 1, 1, 1, 3, 2, 4, 5, 1, 2, 1, 5, 1, 4, 1, 5, 1, 1, 1, 1, 1, 1, 4, 3, 1, 1, 3, 3, 1, 4,
        5, 1, 1, 4, 1, 4, 3, 4, 1, 1, 1, 2, 2, 1, 2, 5, 1, 1, 3, 5, 2, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 5, 4, 1, 1, 1,
        1, 1, 2, 1, 2, 1, 5, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 5, 3, 3, 1, 1, 2, 4, 4, 1, 1, 2, 1,
        1, 3, 1, 1, 1, 1, 2, 3, 4, 1, 1, 2
    ]

    days = 256

    fish_list = simplify_fish_list(fish_list)

    for _ in range(days):
        num_new = 0
        for f in range(len(fish_list)):
            fish_list[f].count_down -= 1
            if fish_list[f].count_down == -1:
                fish_list[f].count_down = 6
                num_new += fish_list[f].num_fish

        fish_list.append(FishGroup(num_new, 8))

    print(sum([f.num_fish for f in fish_list]))

    
if __name__ == '__main__':
    main()
