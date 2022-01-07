class agent:
    def __init__(self, id: int, value: float, src: int, dest: int, speed: int, pos: tuple):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos

    def __str__(self):
        return f'Agent : {self.id}, {self.value}, {self.src}, {self.dest}, {self.speed}, {self.pos}'

    def repr(self):
        return f'Agent : {self.id}, {self.value}, {self.src}, {self.dest}, {self.speed}, {self.pos}'

    def get_pos(self) -> tuple:
        return self.pos
