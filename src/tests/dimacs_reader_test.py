import unittest
from src.dataset_services.dimacs_reader import DimacsReader


class TestDimacsReaderWithoutDescription(unittest.TestCase):
    def setUp(self):
        DIR = "src/tests/testdata_dimacs_graph/no_description"
        self.DR = DimacsReader(DIR)

    def test_read_dimacs_graph_without_description(self):
        name, number_of_nodes, number_of_edges, sources, licence, short_desc = self.DR.read_dimacs_graph("test_example.dimacs")
        self.assertEqual(name, "test_example")
        self.assertEqual(number_of_nodes, 5)
        self.assertEqual(number_of_edges, 10)
        self.assertEqual(sources, [])
        self.assertEqual(licence, None)
        self.assertEqual(short_desc, None)