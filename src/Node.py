import math

class Node:
    def __init__(self, id: int, pos: tuple):
        self.id = id
        self.pos = pos
        self.weight = math.inf
        self.tag = 0

    def get_weight(self):
        return self.weight

    def set_weight(self, data: int):
        self.weight = data



    def get_tag(self):
        return self.tag

    # white = 0 , gey  =1 , black = 2
    def set_tag(self, color: int):
        self.tag = color

    def __repr__(self):
        return f"id: {self.id}, pos: {self.pos} weight: {self.weight}"


    def __lt__(self, other):
        return self.weight < other.weight

if __name__ == '__main__':
    pos = (1, 2, 3)
    node = Node(1, pos)

    print(node.get_weight())
    node.set_weight(0)
#
# print(node.weight)
