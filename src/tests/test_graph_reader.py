
import unittest
from src.file_ui.graph_reader import GraphReader


class TestGraphReader(unittest.TestCase):

    def setUp(self):
        DIR = "src/tests/testdata"
        self.graphreader = GraphReader(DIR)
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

    def test_graph_object_should_have_number_of_nodes_2(self):
        graph_list = self.graphreader.get_graph_list()
        res = None
        for graph in graph_list:
            if graph.name == "gt1.kmer15.(1268000.1270000).V21.E27.cyc64":
                res = graph.nodes

        self.assertEqual(res, 21)

    def test_graph_object_should_have_number_of_edges_2(self):
        graph_list = self.graphreader.get_graph_list()
        res = None
        for graph in graph_list:
            if graph.name == "gt1.kmer15.(1268000.1270000).V21.E27.cyc64":
                res = graph.edges

        self.assertEqual(res, 27)

    def test_graph_object_should_have_list_of_source_files(self):
        graph_list = self.graphreader.get_graph_list()
        for graph in graph_list:
            if graph.name == "gt20.kmer15.(102000.104000).V75.E104.cyc1000":
                res = graph.get_sources()

        self.assertEqual(len(res), 20)

    def test_graph_object_source_list_contains_correct_names(self):
        graph_list = self.graphreader.get_graph_list()
        for graph in graph_list:
            if graph.name == "gt20.kmer15.(102000.104000).V75.E104.cyc1000":
                res = graph.get_sources()
            
        self.assertEqual(res[1], "GCA_000006665.1_ASM666v1.fna")


class TestGraphReaderEmptyDescription(unittest.TestCase):

    def setUp(self):
        DIR = "src/tests/testdata_with_empty_description"
        self.graphreader = GraphReader(DIR)
        self.graphreader.run()

    def test_get_graph_list_should_return_list_of_only_graph_files(self):
        res = self.graphreader.get_graph_list()
        self.assertEqual(len(res), 5)

