class Ship:
    def __init__(self, pos=None, aim=None):
        self.pos = [0, 0]
        if pos is not None:
            self.pos = pos
        self.aim = 0
        if aim is not None:
            self.aim = aim

    def move(self, command):
        action, value = command.split()
        value = int(value)
        match action:
            case "down":
                self.aim += value
            case "up":
                self.aim -= value
            case "forward":
                self.pos[0] += value
                self.pos[1] += value * self.aim
            case _:
                raise ValueError("Invalid command.")

    def __repr__(self):
        return f"Ship(pos={self.pos}, aim={self.aim})"
                
            

def vectorise(command):
    vector = [0, 0]
    match command.split():
        case ["forward", dist]:
            vector[0] += int(dist)
        case ["down", dist]:
            vector[1] += int(dist)
        case ["up", dist]:
            vector[1] -= int(dist)
        case _:
            raise ValueError("Invalid command.")
    return vector


def move(current_pos, command):
    vector = vectorise(command)
    return [sum([a, b]) for a, b in zip(current_pos, vector)]


