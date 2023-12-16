from typing import List, Union


class Cucumber:
    grid: List[List[Union['Cucumber', None]]] = []
    grid_width = 0
    grid_height = 0

    def __init__(self, heard: str, x: int, y: int):
        self.heard = heard
        self.x = x
        self.y = y

        self.grid[x][y] = self

    @property
    def can_move(self) -> bool:
        if self.heard == "v":
            return self.grid[self.x][(self.y + 1) % self.grid_height] is None
        elif self.heard == ">":
            return self.grid[(self.x + 1) % self.grid_width][self.y] is None

    def move(self):
        self.grid[self.x][self.y] = None
        prev_x, prev_y = self.x, self.y
        if self.heard == "v":
            self.y = (self.y + 1) % Cucumber.grid_height
        elif self.heard == ">":
            self.x = (self.x + 1) % Cucumber.grid_width
        if self.grid[self.x][self.y] is not None:
            Cucumber.print_grid()
            raise ValueError(f"Value error, could not move from {prev_x},{prev_y} to {self.x},{self.y}")
        self.grid[self.x][self.y] = self

        #print()
        #Cucumber.print_grid()
        #print(f"{prev_x},{prev_y} to {self.x},{self.y}")
        #pass


    def __repr__(self):
        return self.heard

    @staticmethod
    def print_grid():
        lines = []
        for y in range(Cucumber.grid_height):
            line = ""
            for x in range(Cucumber.grid_width):
                if (c := Cucumber.grid[x][y]) is not None:
                    line += c.heard
                else:
                    line += "."
            lines.append(line)
        print("\n".join(lines))

    @staticmethod
    def build_grid():
        for _x in range(Cucumber.grid_width):
            row = []
            for _y in range(Cucumber.grid_height):
                row.append(None)
            Cucumber.grid.append(row)


def main():
    x_heard: List[Cucumber] = []
    y_heard: List[Cucumber] = []
    with open("input.txt", "r") as fh:
        lines = [line.strip() for line in fh.readlines()]
        Cucumber.grid_height = len(lines)
        Cucumber.grid_width = len(lines[0])
        Cucumber.build_grid()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == ">":
                    x_heard.append(Cucumber(c, x, y))
                elif c == "v":
                    y_heard.append(Cucumber(c, x, y))

    Cucumber.print_grid()
    print()

    can_move: List[Cucumber] = []
    run = True
    n = 0
    while run:
        n += 1
        run = False

        for c in x_heard:
            if c.can_move:
                can_move.append(c)
                run = True
        for c in can_move:
            c.move()

        can_move.clear()

        for c in y_heard:
            if c.can_move:
                can_move.append(c)
                run = True
        for c in can_move:
            c.move()

        can_move.clear()

    Cucumber.print_grid()
    print(n)


if __name__ == '__main__':
    main()
