from abc import ABC
from Node import *
from GraphInterface import *


class DiGraph(GraphInterface, ABC):
    def __init__(self):
        self.MC = 0
        self.nodes = {}
        self.edges_out = {}
        self.edges_in = {}
        self.edges_out.values().__len__()


    def v_size(self) -> int:
        return self.nodes.__len__()

    '''add to new list all edges in graph assuming that edges_out has the same value as edges_in'''
    def e_size(self) -> int:
        e_size_list = []

        for v in self.edges_out:
            for i in self.edges_out[v]:
                e_size_list.append(i)
        return e_size_list.__len__()

    def get_all_v(self) -> dict:
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        if id1 not in self.edges_in:
            print(id1, "not existing in this dict")  # check if exist
        return self.edges_in.get(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.edges_out.get(id1)

    def get_mc(self) -> int:
        return self.MC

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 is id2:  # same in memory
            print("point to the same value in memory")
            return False

        if id1 not in self.nodes.keys():
            print(id1, "not in the graph")
            return False

        if id2 not in self.nodes.keys():
            print(id2, "not in the graph")
            return False

        if id1 in self.edges_out:  # check if this edge exist
            if id2 in self.edges_out.get(id1):
                print("already in graph")
                return False

        if id1 not in self.edges_out:  # create new dict for edge
            self.edges_out[id1] = {}
            self.edges_out[id1].update()
        if id2 not in self.edges_in:
            self.edges_in[id2] = {}
        self.edges_out[id1][id2] = weight
        self.edges_in[id2][id1] = weight
        self.MC += 1

        return True




    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        new_node = Node(node_id, pos)
        if node_id in self.nodes.keys():
            print(node_id, "is already in the graph")
            return False
        else:  # create new node
            self.nodes[node_id] = new_node
            self.MC += 1
            return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self.nodes:
            print(node_id, "not in the graph")
            return False
        else:
            self.nodes.pop(node_id)
            self.MC += 1
            if node_id in self.edges_out:  # check if dict edges contain this id
                self.edges_out.pop(node_id)
                self.MC += 1
            if node_id in self.edges_in:
                self.edges_in.pop(node_id)
                self.MC += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self.nodes:  # check if this node is exist
            print(node_id1, " is not present in the graph")
            return False
        if node_id2 not in self.nodes:
            print(node_id2, " is not present in the graph")
            return False
        if node_id1 in self.edges_out:  # check if our dict of edges contain this node
            if node_id2 in self.edges_out.get(node_id1):  # then check if id1 node have value of id2
                self.edges_out.get(node_id1).pop(node_id2)
                self.edges_in.get(node_id2).pop(node_id1)
                self.MC += 1
                return True
            return False
        print("this edge is missing in graph")
        return False

    def __str__(self):
        return f"nodes: {self.nodes}\nedges: {self.edges_out}"
