import os
from unittest import TestCase
from DiGraph import *
from GraphAlgo import *
import numbers


class TestGraphAlgo(TestCase):
    def test_get_graph(self):
        graph: GraphInterface = DiGraph()
        """# INIT graph with nodes [5-9] and edges {5-6} {5-9} {9-5} {8-7} {7-8} {7-9}"""
        for i in range(5, 10):
            graph.add_node(i, (0, 0, 0))
        graph.add_edge(5, 6, 2)
        graph.add_edge(5, 9, 3)
        graph.add_edge(9, 5, 4)
        graph.add_edge(8, 7, 5)
        graph.add_edge(7, 8, 6)
        graph.add_edge(7, 9, 7)
        graph_algo: GraphAlgoInterface = GraphAlgo(graph)
        graph_temp: GraphInterface = graph_algo.get_graph()

        """# check if all databases are the same. (by values). expected -> TRUE"""

        print("get_graph -> test 1")
        """# e_size method"""
        self.assertEqual(graph_temp.e_size(), graph.e_size())
        print("Passed!")

        print("get_graph -> test 2")
        """# v_size method"""
        self.assertEqual(graph_temp.v_size(), graph.v_size())
        print("Passed!")

        print("get_graph -> test 3")
        """# get_all_v method"""
        self.assertEqual(graph_temp.get_all_v(), graph.get_all_v())
        print("Passed!")

        print("get_graph -> test 4")
        """# all_out_edges_of_node method. node_checked (5)"""
        self.assertEqual(graph_temp.all_out_edges_of_node(5), graph.all_out_edges_of_node(5))
        print("Passed!")

        print("get_graph -> test 5")
        """# all_in_edges_of_node method. node_checked (9)"""
        self.assertEqual(graph_temp.all_out_edges_of_node(9), graph.all_out_edges_of_node(9))
        print("Passed!")

        """# try to remove node from original graph and check differences with temp_graph. should effect both graphs."""
        graph.remove_node(5)
        print("get_graph -> test 6")
        """# v_size method"""
        self.assertEqual(graph_temp.v_size(), graph.v_size())
        print("Passed!")

        print("get_graph -> test 7")
        """# e_size method"""
        self.assertEqual(graph_temp.e_size(), graph.e_size())
        print("Passed All!")

    def test_load_from_json(self):
        graph: GraphInterface = DiGraph()
        graph_algo: GraphAlgoInterface = GraphAlgo(graph)
        graph_algo.load_from_json("../data/A0.json")
        graph = graph_algo.get_graph()

        print("load_from_json -> test 1")
        """# try to add to the init graph 2 nodes that exist in json file. expected -> FALSE"""
        self.assertFalse(graph.add_node(0))
        self.assertFalse(graph.add_node(1))

        print("load_from_json -> test 2")
        """# try to add edge that exist in json file. expected -> FALSE"""
        self.assertFalse(graph.add_edge(0, 1, 0))

        print("load_from_json -> test 3")
        """# try to remove edge from graph that exist in json file. expected -> TRUE"""
        self.assertTrue(graph.remove_edge(0, 1))

        print("load_from_json -> test 4")
        """# try to remove node that exist in json file. expected -> TRUE"""
        self.assertTrue(graph.remove_node(9))

        print("load_from_json -> test 5")
        """# try to remove node that do not exist in json file. expected -> FALSE"""
        self.assertFalse(graph.remove_node(99))

        """# manual INIT new graph that is identical to "T0.json" file"""
        graph_t: GraphInterface = DiGraph()
        graph_t_algo: GraphAlgoInterface = GraphAlgo(graph_t)
        graph_t_algo.load_from_json("../data/T0.json")
        graph_t = graph_t_algo.get_graph()

        man_graph: GraphInterface = DiGraph()
        for i in range(4):
            man_graph.add_node(i)
        man_graph.add_edge(0, 1, 1)
        man_graph.add_edge(1, 0, 1.1)
        man_graph.add_edge(1, 2, 1.3)
        man_graph.add_edge(1, 3, 1.8)
        man_graph.add_edge(2, 3, 1.1)

        """# compare all databases between the two graphs. expected -> TRUE on each"""

        print("load_from_json -> test 6")
        """# e_size method"""
        self.assertEqual(man_graph.e_size(), graph_t.e_size())
        print("Passed!")

        print("load_from_json -> test 7")
        """# v_size method"""
        self.assertEqual(man_graph.v_size(), graph_t.v_size())
        print("Passed!")

        print("load_from_json -> test 8")
        """# get_all_v method"""
        self.assertEqual(man_graph.get_all_v().__len__(), graph_t.get_all_v().__len__())
        print("Passed!")

        print("load_from_json -> test 9")
        """# all_out_edges_of_node method. node_checked (5)"""
        self.assertEqual(man_graph.all_out_edges_of_node(1), graph_t.all_out_edges_of_node(1))
        print("Passed!")

        print("load_from_json -> test 10")
        """# all_in_edges_of_node method. node_checked (9)"""
        self.assertEqual(man_graph.all_out_edges_of_node(3), graph_t.all_out_edges_of_node(3))
        print("Passed!")

        """# load_json to already initialized graph. expected -> clear the existed graph and make new one as json"""
        new_graph: GraphInterface = DiGraph()
        """# INIT graph with nodes [5-9] and edges {5-6} {5-9} {9-5} {8-7} {7-8} {7-9}"""
        for i in range(5, 10):
            new_graph.add_node(i, (0, 0, 0))
        new_graph.add_edge(5, 6, 2)
        new_graph.add_edge(5, 9, 3)
        new_graph.add_edge(9, 5, 4)
        new_graph.add_edge(8, 7, 5)
        new_graph.add_edge(7, 8, 6)
        new_graph.add_edge(7, 9, 7)
        new_graph_algo: GraphAlgoInterface = GraphAlgo(new_graph)
        new_graph_algo.load_from_json("../data/T0.json")
        new_graph = new_graph_algo.get_graph()

        """# try to remove node_id 5. the graph that described in T0.json does not have node_id 5 like the previous 
        graph. expected -> FALSE """

        print("load_from_json -> test 11")
        self.assertFalse(new_graph.remove_node(5))
        print("Passed!")

        print("load_from_json -> test 12")
        """# INIT graph to compare nodes positions."""
        graph_comp_1: GraphInterface = DiGraph()
        graph_algo_comp_1: GraphAlgoInterface = GraphAlgo(graph_comp_1)
        graph_algo_comp_1.load_from_json("../data/A0.json")
        graph_comp_1 = graph_algo_comp_1.get_graph()
        pos_list_1 = []
        for key in graph_comp_1.get_all_v():
            node_pos = graph_comp_1.get_all_v().get(key).pos
            pos_list_1.append(node_pos)

        """# INIT new graph like "graph_comp_1" and compare nodes positions. expected -> TRUE"""
        graph_comp_2: GraphInterface = DiGraph()
        graph_algo_comp_2: GraphAlgoInterface = GraphAlgo(graph_comp_2)
        graph_algo_comp_2.load_from_json("../data/A0.json")
        graph_comp_2 = graph_algo_comp_2.get_graph()
        pos_list_2 = []
        for key in graph_comp_2.get_all_v():
            node_pos = graph_comp_2.get_all_v().get(key).pos
            pos_list_2.append(node_pos)

        print("FIRST", pos_list_1)
        print("SECOND", pos_list_2)
        self.assertEqual(pos_list_1, pos_list_2)
        print("Passed!")

        print("load_from_json -> test 13")
        """# check if the positions are represented as numbers (and not char, string etc..). expected -> TRUE"""
        for i in range(pos_list_1.__len__()):
            self.assertTrue(isinstance(pos_list_1.__getitem__(i)[0], numbers.Number))
            self.assertTrue(isinstance(pos_list_1.__getitem__(i)[1], numbers.Number))
            self.assertTrue(isinstance(pos_list_1.__getitem__(i)[2], numbers.Number))
        print("Passed All!")

    def test_save_to_json(self):
        graph: GraphInterface = DiGraph()
        graph_algo: GraphAlgoInterface = GraphAlgo(graph)

        """# load A0.json to graph and then save it as "A0.saved.json" ."""
        graph_algo.load_from_json("../data/A0.json")
        graph = graph_algo.get_graph()
        graph_algo.save_to_json("../data/A0_saved.json")

        print("save_to_json -> test 1")
        """# load the saved file ("A0_saved.json") . expected -> True"""
        graph_temp: GraphInterface = DiGraph()
        graph_algo_temp: GraphAlgoInterface = GraphAlgo(graph_temp)
        self.assertTrue(graph_algo_temp.load_from_json("../data/A0_saved.json"))
        graph_temp = graph_algo_temp.get_graph()
        os.remove("../data/A0_saved.json")

        """# compare between the two graphs."""
        print("save_to_json -> test 2")
        """# e_size method"""
        self.assertEqual(graph_temp.e_size(), graph.e_size())
        print("Passed!")

        print("save_to_json -> test 3")
        """# v_size method"""
        self.assertEqual(graph_temp.v_size(), graph.v_size())
        print("Passed!")

        print("save_to_json -> test 4")
        """# get_all_v method"""
        self.assertEqual(graph_temp.get_all_v().__len__(), graph.get_all_v().__len__())
        print("Passed!")

        print("save_to_json -> test 5")
        """# all_out_edges_of_node method. node_checked (5)"""
        self.assertEqual(graph_temp.all_out_edges_of_node(1), graph.all_out_edges_of_node(1))
        print("Passed!")

        print("save_to_json -> test 6")
        """# all_in_edges_of_node method. node_checked (9)"""
        self.assertEqual(graph_temp.all_out_edges_of_node(3), graph.all_out_edges_of_node(3))
        print("Passed All!")

    def test_shortest_path(self):

        graph: GraphInterface = DiGraph()
        graph_algo: GraphAlgoInterface = GraphAlgo(graph)

        for i in range(6):
            graph.add_node(i)
        graph.add_edge(0, 2, 5)
        graph.add_edge(1, 0, 42)
        graph.add_edge(1, 3, 5)
        graph.add_edge(2, 0, 7)
        graph.add_edge(2, 5, 1)
        graph.add_edge(3, 1, 11)
        graph.add_edge(3, 2, 1)
        graph.add_edge(3, 4, 3)
        graph.add_edge(4, 5, 1)
        graph.add_edge(5, 3, 5)

        print("shortest_path -> test 1")
        """# shortest path from src:4 to dest:0. expected -> value (14) path{4,5,3,2,0}"""
        self.assertEqual((14, [4, 5, 3, 2, 0]), graph_algo.shortest_path(4, 0))
        print("Passed!")

        print("shortest_path -> test 2")
        """# shortest path from src:0 to dest:1. expected -> value (22) path{0,2,5,3,1}"""
        self.assertEqual((22, [0, 2, 5, 3, 1]), graph_algo.shortest_path(0, 1))
        print("Passed!")

        print("shortest_path -> test 3")
        """# shortest path from src:2 to dest:1. expected -> value (17) path{2,5,3,1}"""
        self.assertEqual((17, [2, 5, 3, 1]), graph_algo.shortest_path(2, 1))
        print("Passed!")

        print("shortest_path -> test 4")
        """# shortest path from src:10 (do not exist in graph) dest:2. expected -> value (infinity) path{}"""
        self.assertEqual((float('inf'), []), graph_algo.shortest_path(10, 2))
        print("Passed!")

        """# INIT graph T0.json"""
        graph_t0: GraphInterface = DiGraph()
        graph_t0_algo: GraphAlgoInterface = GraphAlgo(graph_t0)
        graph_t0_algo.load_from_json("../data/T0.json")

        print("shortest_path -> test 5 <T0.json>")
        """# shortest path in T0.json from src:0 des:3. expected -> value(2.8) path {0,1,3}"""
        self.assertEqual((2.8, [0, 1, 3]), graph_t0_algo.shortest_path(0, 3))
        print("Passed!")

        print("shortest_path -> test 6 <T0.json>")
        """# shortest path in T0.json from src:3 dest:0. expected -> value(infinity) path{}"""
        self.assertEqual((float('inf'), []), graph_t0_algo.shortest_path(3, 0))
        print("Passed!")

        print("shortest_path -> test 7")
        """# INIT graph with node starting at id 5 instead of 0."""
        graph_last: GraphInterface = DiGraph()
        graph_last_algo: GraphAlgoInterface = GraphAlgo(graph_last)

        for i in range(5, 11):
            graph_last.add_node(i)

        graph_last.add_edge(5, 6, 5)
        graph_last.add_edge(5, 7, 11)
        graph_last.add_edge(6, 7, 3)
        graph_last.add_edge(6, 9, 18)
        graph_last.add_edge(6, 10, 11)
        graph_last.add_edge(7, 5, 6)
        graph_last.add_edge(7, 9, 21)
        graph_last.add_edge(8, 9, 1)
        graph_last.add_edge(8, 10, 7)
        graph_last.add_edge(9, 6, 1)
        graph_last.add_edge(10, 8, 13)

        """# testing on src:8 dest:5. expected -> value(11) path {8, 9, 6, 7, 5}"""
        self.assertEqual((11, [8, 9, 6, 7, 5]), graph_last_algo.shortest_path(8, 5))
        print("Passed All!")

    def test_center_point(self):

        graph: GraphInterface = DiGraph()
        graph_algo: GraphAlgoInterface = GraphAlgo(graph)

        print("center_point -> test 1 <A0.json>")
        """# loading A0.json and check its center. expected -> (7, 6.806805834715163)"""
        graph_algo.load_from_json("../data/A0.json")
        self.assertEqual((7, 6.806805834715163), graph_algo.centerPoint())
        print("Passed!")

        print("center_point -> test 2 <A1.json>")
        """# loading A1.json and check its center. expected -> (8, 9.925289024973141)"""
        graph_algo.load_from_json("../data/A1.json")
        self.assertEqual((8, 9.925289024973141), graph_algo.centerPoint())
        print("Passed!")

        print("center_point -> test 3 <A2.json>")
        """# loading A2.json and check its center. expected -> (0, 7.819910602212574)"""
        graph_algo.load_from_json("../data/A2.json")
        self.assertEqual((0, 7.819910602212574), graph_algo.centerPoint())
        print("Passed!")

        print("center_point -> test 4 <A3.json>")
        """# loading A3.json and check its center. expected -> (2, 8.182236568942237)"""
        graph_algo.load_from_json("../data/A3.json")
        self.assertEqual((2, 8.182236568942237), graph_algo.centerPoint())
        print("Passed!")

        print("center_point -> test 5 <A4.json>")
        """# loading A4.json and check its center. expected -> (6, 8.071366078651435)"""
        graph_algo.load_from_json("../data/A4.json")
        self.assertEqual((6, 8.071366078651435), graph_algo.centerPoint())
        print("Passed!")

        print("center_point -> test 6 <A5.json>")
        """# loading A5.json and check its center. expected -> (40, 9.291743173960954)"""
        graph_algo.load_from_json("../data/A5.json")
        self.assertEqual((40, 9.291743173960954), graph_algo.centerPoint())
        print("Passed All!")

    def test_tsp(self):
        graph: GraphInterface = DiGraph()
        graph_algo: GraphAlgoInterface = GraphAlgo(graph)

        """# INIT new connected graph"""
        for i in range(1, 5):
            graph.add_node(i)
        graph.add_edge(1, 2, 10)
        graph.add_edge(1, 3, 15)
        graph.add_edge(1, 4, 20)
        graph.add_edge(2, 1, 10)
        graph.add_edge(2, 4, 25)
        graph.add_edge(2, 3, 35)
        graph.add_edge(3, 2, 35)
        graph.add_edge(3, 4, 30)
        graph.add_edge(3, 1, 15)
        graph.add_edge(4, 1, 20)
        graph.add_edge(4, 2, 25)
        graph.add_edge(4, 3, 30)

        print("TSP -> test 1")
        """# test tsp method on sorted list [1,2,3,4]. expected -> ([3,1,2,4], 50)"""
        self.assertEqual(([3, 1, 2, 4], 50), graph_algo.TSP([1, 2, 3, 4]))
        print("Passed!")

        print("TSP -> test 2")
        """# test tsp method on unsorted list [2,1,3,4]. expected -> ([3,1,2,4], 50)"""
        self.assertEqual(([3, 1, 2, 4], 50), graph_algo.TSP([2, 1, 3, 4]))
        print("Passed All!")

    # def test_plot_graph(self):
    #     self.fail()


