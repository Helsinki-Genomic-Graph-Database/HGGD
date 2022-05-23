"""
import unittest
from file_ui.graphReader import GraphReader

class TestGraphReader(unittest.TestCase):

    def setUp(self):
        self.graphreader = GraphReader()
        self.graphreader.run()

    def test_get_graph_list_should_return_list(self):
        res = self.graphreader.get_graph_list()
        self.assertEqual(len(res), 5)

    def test_graph_object_should_have_number_of_nodes(self):
        graph_list = self.graphreader.get_graph_list()
        res = None
        for graph in graph_list:
            if graph.name == "gt1.kmer15.(1466000.1468000).V26.E35.cyc240":
                res = graph.nodes

        self.assertEqual(res, 26)

    def test_graph_object_should_have_number_of_edges(self):
        list = self.graphreader.get_graph_list()
        res = None
        for graph in list:
            if graph.name == "gt1.kmer15.(1466000.1468000).V26.E35.cyc240":
                res = graph.edges

        self.assertEqual(res, 35)
<<<<<<< HEAD

    def test_graph_object_should_have_number_of_nodes_2(self):
        graph_list = self.graphreader.get_graph_list()
        res = None
        for graph in graph_list:
            if graph.name == "gt1.kmer15.(1268000.1270000).V21.E27.cyc64":
                res = graph.nodes

        self.assertEqual(res, 21)

    def test_graph_object_should_have_number_of_edges_2(self):
        list = self.graphreader.get_graph_list()
        res = None
        for graph in list:
            if graph.name == "gt1.kmer15.(1268000.1270000).V21.E27.cyc64":
                res = graph.edges

        self.assertEqual(res, 27)

=======
"""
>>>>>>> e85e5e524e0771ce9b8b6a11c8dd4cdb4c7b8c23
