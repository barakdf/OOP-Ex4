class agent:
    def __init__(self, id: int, value: float, src: int, dest: int, speed: int, pos: tuple, targets: dict):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos

        self.explore: list = [self.src]
        self.targets = targets
        self.weight = 0
        self.attack_mode = False
        self.pokemon_radar = {}

    def __str__(self):
        return f'Agent : {self.id}, {self.value}, {self.src}, {self.dest}, {self.speed}, {self.pos}'

    def __repr__(self):
        return f'Agent : {self.id}, {self.value}, {self.src}, {self.dest}, {self.speed}, {self.pos}'

    def get_pos(self) -> tuple:
        float_pos = (float(self.pos[0]), float(self.pos[1]), float(self.pos[2]))
        return float_pos
