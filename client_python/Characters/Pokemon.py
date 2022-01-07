class pokemon:
    def __init__(self, value: int, edge_type: int, pos: tuple):
        self.value = value
        self.edge_type = edge_type
        self.pos = pos

        self.p_src = None
        self.p_dest = None


    def __str__(self):
        return f'Pokemon: {self.value}, {self.edge_type}, {self.pos}, {self.p_src}, {self.p_dest}'

    def repr(self):
        return f'Pokemon: {self.value}, {self.edge_type}, {self.pos}, {self.p_src}, {self.p_dest}'
