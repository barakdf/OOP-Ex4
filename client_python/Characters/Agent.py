class agent:
    def __init__(self, id: int, value: float, src: int, dest: int, speed: int, pos: tuple, targets: dict):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos

        self.explore = [self.src]
        self.targets = targets
        self.weight = 0

    def __str__(self):
        return f'Agent : {self.id}, {self.value}, {self.src}, {self.dest}, {self.speed}, {self.pos}'

    def __repr__(self):
        return f'Agent : {self.id}, {self.value}, {self.src}, {self.dest}, {self.speed}, {self.pos}'

    def get_pos(self) -> tuple:
        return self.pos
