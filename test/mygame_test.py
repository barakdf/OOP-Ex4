from unittest import TestCase
from client_python.Characters.MyGame import MyGame
from client_python.src.DiGraph import DiGraph
from client_python.Characters.Pokemon import pokemon
from client_python.src.Node import Node


class myGameTest(TestCase):
    graph_1: DiGraph = DiGraph()
    """# INIT graph with nodes [5-9] and edges {5-6} {5-9} {9-5} {8-7} {7-8} {7-9}"""
    for i in range(5, 10):
        graph_1.add_node(i, (0, 0, 0))
        game: MyGame = MyGame(graph_1)

    def test_is_on(self):
        po: tuple = (1, 2, 0)
        po2: tuple = (5, 4, 0)
        pok: pokemon = pokemon(5, -1, (1, 2, 0))

        print("test_is_on -> test 1")
        self.assertEqual(self.game.is_on(pok.pos, po, po2), 0.0)
        print("Passed!")


    

