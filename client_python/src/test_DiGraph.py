from unittest import TestCase
from DiGraph import *


class TestDiGraph(TestCase):
    def test_v_size(self):
        graph_1: DiGraph = DiGraph()

        print("v_size -> test 1")
        """# when the graph just init number of nodes should be 0."""
        self.assertEqual(0, graph_1.v_size())
        print("Passed!")

        print("v_size -> test 2")
        """# adding 2 new nodes, number of nodes should be 2."""
        graph_1.add_node(1, pos=(1, 2, 0))
        graph_1.add_node(2, pos=(4, 5, 0))
        self.assertEqual(2, graph_1.v_size())
        print("Passed!")

        print("v_size -> test 3")
        """# adding new node with existing id in collection, number id should remain as before (2)."""
        graph_1.add_node(1, pos=(1, 3, 0))
        self.assertEqual(2, graph_1.v_size())
        print("Passed!")

        print("v_size -> test 4")
        """# adding new node without pos, should increase the node size by one (total - 3)."""
        graph_1.add_node(3)
        self.assertEqual(3, graph_1.v_size())
        print("Passed!")

        print("v_size -> test 5")
        """# init new graph, should not be affected by previous graph, size = 0."""
        graph_2: DiGraph = DiGraph()
        self.assertEqual(0, graph_2.v_size())
        print("Passed!")

        ## ------> FAILED FROM HERE!
        print("v_size -> test 6")
        """# try to remove one existing node, node size should be (2)."""
        graph_1.remove_node(1)
        self.assertEqual(2, graph_1.v_size())
        print("Passed!")

        print("v_size -> test 7")
        """# try to remove the same node we removed before, should not effect updated size (2)."""
        graph_1.remove_node(1)
        self.assertEqual(2, graph_1.v_size())
        print("Passed!")

        print("v_size -> test 8")
        """# try to remove a known non-existing node, should not effect node_size."""
        graph_1.remove_node(99999)
        self.assertEqual(2, graph_1.v_size())
        print("Passed All!")

    def test_e_size(self):
        graph_1: DiGraph = DiGraph()

        print("e_size -> test 1")
        """# when the graph just init number of EDGES should be 0."""
        self.assertEqual(0, graph_1.e_size())
        print("Passed!")

        print("e_size -> test 2")
        """# adding 1 new edge with two different nodes_id, number of edges should be 1."""
        graph_1.add_node(1, (0, 0, 0))
        graph_1.add_node(2, (0, 0, 0))
        graph_1.add_edge(1, 2, 0)
        self.assertEqual(1, graph_1.e_size())
        print("Passed!")

        print("e_size -> test 3")
        """# try to connect node to himself, should not add this edge and to not increase edge_size."""
        graph_1.add_edge(1, 1, 20)
        self.assertEqual(1, graph_1.e_size())
        print("Passed!")

        print("e_size -> test 4")
        """# add 2 new nodes and connect between both directions and add 2 new edges (should be 3 total)."""
        graph_1.add_node(3, (0, 0, 0))
        graph_1.add_node(4, (0, 0, 0))
        graph_1.add_edge(3, 4, 10)
        graph_1.add_edge(4, 3, 10)
        self.assertEqual(3, graph_1.e_size())
        print("Passed!")

        print("e_size -> test 5")
        """# try to connect existing edge, edge size should remain the same (3)."""
        graph_1.add_edge(3, 4, 10)
        self.assertEqual(3, graph_1.e_size())
        print("Passed!")

        ## --------> FAILED FROM HERE!

        print("e_size -> test 6")
        """ # try to remove valid edge from graph, edge size should be (2) [decreased by 1]
            # node size should not effected (4)."""
        graph_1.remove_edge(3, 4)
        self.assertEqual(2, graph_1.e_size())
        self.assertEqual(4, graph_1.v_size())
        print("Passed!")

        print("e_size -> test 7")
        """ # try to remove invalid edge (src == dest), should not effect edge_size (2)
            # and node size(4)."""
        graph_1.remove_edge(1, 1)
        self.assertEqual(2, graph_1.e_size())
        self.assertEqual(4, graph_1.v_size())
        print("Passed!")

        print("e_size -> test 8")
        """# remove non existing edge, should not effect edge_size (2) and node size(4)."""
        graph_1.remove_edge(2, 1)
        self.assertEqual(2, graph_1.e_size())
        graph_1.remove_edge(100000, 999999)
        self.assertEqual(2, graph_1.e_size())
        self.assertEqual(4, graph_1.v_size())
        print("Passed!")

        print("e_size -> test 9")
        """# remove node with ~one connected edge~ from graph, should decrease e_size by one (0)"""
        graph_2: DiGraph = DiGraph()
        graph_2.add_node(1)
        graph_2.add_node(2)
        graph_2.add_edge(1, 2, 0)
        self.assertEqual(1, graph_2.e_size())
        graph_2.remove_node(1)
        self.assertEqual(0, graph_2.e_size())
        print("Passed All!")

    def test_get_all_v(self):
        graph_1: DiGraph = DiGraph()
        """# ---> INIT new graph with nodes [0 - 4]"""
        for i in range(5):
            graph_1.add_node(i, (0, 0, 0))

        print("get_all_v -> test 1")
        """# expected to return dict with all nodes [0-4]"""
        expected = {}
        for i in range(5):
            expected[i] = Node(i, (0, 0, 0))
        self.assertEqual(expected.keys(), graph_1.get_all_v().keys())
        self.assertEqual(expected.values().__len__(), graph_1.get_all_v().values().__len__())
        print("Passed!")

        print("get_all_v -> test 2")
        """# try to remove node_id -4, expected -> same list without - 4 """
        graph_1.remove_node(4)
        expected.pop(4)
        self.assertEqual(expected.keys(), graph_1.get_all_v().keys())
        print("Passed All!")

    def test_all_in_edges_of_node(self):
        graph_1: DiGraph = DiGraph()
        """# INIT graph with nodes [5-9] and edges {5-6} {5-9} {9-5} {8-7} {7-8} {7-9}"""
        for i in range(5, 10):
            graph_1.add_node(i, (0, 0, 0))
        graph_1.add_edge(5, 6, 2)
        graph_1.add_edge(5, 9, 3)
        graph_1.add_edge(9, 5, 4)
        graph_1.add_edge(8, 7, 5)
        graph_1.add_edge(7, 8, 6)
        graph_1.add_edge(7, 9, 7)

        print("all_in_edges_of_node -> test 1")
        """# check all in edges to node 5. expected -> {9-5} edge represent as {other node(9): weight(4)}"""
        expected_in = {9: 4}
        self.assertEqual(expected_in, graph_1.all_in_edges_of_node(5))
        print("Passed!")

        print("all_in_edges_of_node -> test 2")
        """# check all in edges to node 9, expected -> {5-9}, {7-9}"""
        expected_in.clear()
        expected_in = {5: 3, 7: 7}
        self.assertEqual(expected_in, graph_1.all_in_edges_of_node(9))
        print("Passed!")

        print("all_in_edges_of_node -> test 3")
        """# remove edge {5-9} and check all in edges to node 9. expected -> {7-9}"""
        graph_1.remove_edge(5, 9)
        expected_in.pop(5)
        self.assertEqual(expected_in, graph_1.all_in_edges_of_node(9))
        print("Passed!")

        print("all_in_edges_of_node -> test 4")
        """# try get all in edges from non-existing node (99). expected ->None + PRINT("node is missing in graph")"""
        self.assertEqual(None, graph_1.all_in_edges_of_node(99))
        print("Passed All!")

    def test_all_out_edges_of_node(self):
        graph_1: DiGraph = DiGraph()
        """# INIT graph with nodes [5-9] and edges {5-6} {5-9} {9-5} {8-7} {7-8} {7-9}"""
        for i in range(5, 10):
            graph_1.add_node(i, (0, 0, 0))
        graph_1.add_edge(5, 6, 2)
        graph_1.add_edge(5, 9, 3)
        graph_1.add_edge(9, 5, 4)
        graph_1.add_edge(8, 7, 5)
        graph_1.add_edge(7, 8, 6)
        graph_1.add_edge(7, 9, 7)

        print("all_out_edges_of_node -> test 1")
        """# check all out edges to node 5, expected -> {5-6} {5-9}"""
        expected_out = {6: 2, 9: 3}
        self.assertEqual(expected_out, graph_1.all_out_edges_of_node(5))
        print("Passed!")

        print("all_out_edges_of_node -> test 2")
        """# remove edge {5-6} and check again on node 5. expected -> {5-9}"""
        graph_1.remove_edge(5, 6)
        expected_out.pop(6)
        self.assertEqual(expected_out, graph_1.all_out_edges_of_node(5))
        print("Passed!")

        print("all_out_edges_of_node -> test 3")
        """# try get all out edges from non-existing node (99). expected ->None + PRINT("node is missing in graph")"""
        self.assertEqual(None, graph_1.all_out_edges_of_node(99))
        print("Passed All!")

    def test_get_mc(self):
        graph_1: DiGraph = DiGraph()

        print("get_mc -> test 1")
        """# adding 10 new nodes. expected mc+=10 (total 10)"""
        for i in range(10):
            graph_1.add_node(i, (0, 0, 0))

        self.assertEqual(10, graph_1.get_mc())
        print("Passed!")

        print("get_mc -> test 2")
        """# adding same nodes twice [0 - 4]"""
        graph_2: DiGraph = DiGraph()
        for i in range(0, 5):
            graph_2.add_node(i, (0, 0, 0,))
        for i in range(10):
            graph_2.add_node(i, (0, 0, 0,))
        self.assertEqual(10, graph_2.get_mc())
        print("Passed!")

        print("get_mc -> test 3")
        """# removing all nodes from graph_2. expected -> mc+=10 (total 20)"""
        for i in range(10):
            graph_2.remove_node(i)

        self.assertEqual(20, graph_2.get_mc())
        print("Passed!")

        print("get_mc -> test 4")
        """# adding 10 valid edges to graph_1 (notice edge 1-1 should not count) . expected ->  mc+=9 (total 19)"""
        for i in range(10):
            graph_1.add_edge(1, i, 2)
        self.assertEqual(19, graph_1.get_mc())
        print("Passed!")

        print("get_mc -> test 5")
        """# adding 5 invalid edges to graph_1. expected -> mc+=0 (total 19)"""
        for i in range(90, 95):
            graph_1.add_edge(20, i, 2)
        self.assertEqual(19, graph_1.get_mc())
        print("Passed!")

        print("get_mc -> test 6")
        """# remove valid edge from graph_1. expected -> mc += 1 (total 20)"""
        graph_1.remove_edge(1, 2)
        self.assertEqual(20, graph_1.get_mc())
        print("Passed!")

        print("get_mc -> test 7")
        """# remove invalid edge from graph_1. expected -> mc+=0 (total 20)"""
        graph_1.remove_edge(99, 100)
        self.assertEqual(20, graph_1.get_mc())
        print("Passed All!")

    def test_add_edge(self):

        graph_1: DiGraph = DiGraph()
        """#------> init graph with nodes [0,1,2,3,4] """
        for i in range(5):
            graph_1.add_node(i)

        print("add_edge -> test 1")
        """# adding valid edges. expected -> TRUE """
        self.assertTrue(graph_1.add_edge(1, 2, 0))
        self.assertTrue(graph_1.add_edge(2, 3, 0))
        self.assertTrue(graph_1.add_edge(3, 4, 0))
        print("Passed!")

        print("add_edge -> test 2")
        """adding edge with one of nodes missing in the graph. expected -> FALSE + PRINT("node is missing in graph")"""
        self.assertFalse(graph_1.add_edge(4, 5, 0))
        print("Passed!")

        print("add_edge -> test 3")
        """adding edge with both of nodes missing in the graph. expected -> FALSE + PRINT("node is missing in graph")"""
        self.assertFalse(graph_1.add_edge(99, 100, 0))
        print("Passed!")

        print("add_edge -> test 4")
        """adding edge that already exist in graph. expected -> FALSE + PRINT("Edge already exist in graph) """
        self.assertFalse(graph_1.add_edge(1, 2, 0))
        print("Passed!")

        print("add_edge -> test 5")
        """remove edge from graph and then adding it back. expected -> TRUE """
        graph_1.remove_edge(1, 2)
        self.assertTrue(graph_1.add_edge(1, 2, 0))
        print("Passed All!")

    def test_add_node(self):
        graph_1: DiGraph = DiGraph()

        print("add_edge -> test 1")
        """# adding one valid node. expected -> TRUE """
        self.assertTrue(graph_1.add_node(1, (0, 0, 0)))
        print("Passed!")

        print("add_edge -> test 2")
        """# adding the same existing node. expected -> FALSE + print("node id already exists") """
        self.assertFalse(graph_1.add_node(1, (0, 0, 0)))
        print("Passed!")

        print("add_edge -> test 3")
        """# removing node from graph and the adding it back. expected -> TRUE """
        graph_1.remove_node(1)
        self.assertTrue(graph_1.add_node(1, (0, 0, 0)))
        print("Passed!")

        print("add_edge -> test 4")
        """# adding new node with same pos as another. expected -> TRUE """
        self.assertTrue(graph_1.add_node(2, (0, 0, 0)))
        print("Passed!")

        print("add_edge -> test 5")
        """# adding new node without declare pos. expected -> True """
        self.assertTrue(graph_1.add_node(3))
        print("Passed All!")

    def test_remove_node(self):

        graph_1: DiGraph = DiGraph()
        """#----> INIT graph with nodes [0-4]"""
        for i in range(5):
            graph_1.add_node(i)

        print("remove_node -> test 1")
        """# remove node that does not exist in graph. expected -> FALSE + PRINT("node is missing in graph")"""
        self.assertFalse(graph_1.remove_node(99))
        print("Passed!")

        print("remove_node -> test 2")
        """# remove one existing node from graph. expected -> TRUE """
        self.assertTrue(graph_1.remove_node(1))
        print("Passed!")

        print("remove_node -> test 3")
        """# try to remove the same node from above. expected -> FALSE + PRINT("node is missing in graph") """
        self.assertFalse(graph_1.remove_node(1))
        print("Passed All!")

    def test_remove_edge(self):
        graph_1: DiGraph = DiGraph()
        """#----> INIT graph with nodes [0-4] and edges [{1-2} {2-1} {1-3} {2-3} {2-4} {4-1}"""
        for i in range(5):
            graph_1.add_node(i)
        graph_1.add_edge(1, 2, 0)
        graph_1.add_edge(2, 1, 0)
        graph_1.add_edge(1, 3, 0)
        graph_1.add_edge(2, 3, 0)
        graph_1.add_edge(2, 4, 0)
        graph_1.add_edge(4, 1, 0)

        print("remove_edge -> test 1")
        """# try to remove edge {1-2}. expected -> TRUE """
        self.assertTrue(graph_1.remove_edge(node_id1=1, node_id2=2))
        print("Passed!")

        print("remove_edge -> test 2")
        """try to remove again the same edge {1,2}. expected -> FALSE + PRINT("this edge is missing in graph")"""
        self.assertFalse(graph_1.remove_edge(1, 2))
        print("Passed!")

        print("remove_edge -> test 3")
        """# try to remove opposite direction from prev edge ({2-1}). expected -> TRUE """
        self.assertTrue(graph_1.remove_edge(2, 1))
        print("Passed!")

        print("remove_edge -> test 4")
        """try to remove edge that do no exist in graph. expected -> FALSE + PRINT("this edge is missing in graph")"""
        self.assertFalse(graph_1.remove_edge(99, 93))
        print("Passed All!")


