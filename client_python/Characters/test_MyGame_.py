from unittest import TestCase
from client_python.Characters.MyGame import MyGame
from client_python.src.DiGraph import DiGraph
from client_python.Characters.Pokemon import pokemon
from client_python.src.Node import Node
from client_python.src.GraphAlgo import GraphAlgo


# class myGameTest(TestCase):
#     graph_1: DiGraph = DiGraph()
#     graph: GraphAlgo = GraphAlgo(graph_1)
#     graph.load_from_json("C:\\Users\\97252\\Documents\\GitHub\\OOP-Ex4\\data\\A0")
#
#     # for i in range(5, 10):
#     #     graph_1.add_node(i, (0, 0, 0))
#     game: MyGame = MyGame(graph.get_graph())
#
#     def test_is_on(self):
#         po: tuple = (1, 2, 0)
#         po2: tuple = (5, 4, 0)
#         pok: pokemon = pokemon(5, -1, (1, 2, 0))
#
#         print("test_is_on -> test 1")
#         self.assertEqual(self.game.is_on(pok.pos, po, po2), 0.0)
#         print("Passed!")
#
#     def test_find_edge(self):
#
#         print(self.graph.get_graph())
#         # pok: pokemon = pokemon(1, -1, (35.19565793847981, 32.10567199049591, 0.0))
#         # ans = ()
#         #
#         # self.assertEqual(self.game.find_edge(pok.pos, -1), ans)
