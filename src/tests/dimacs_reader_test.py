import unittest
from src.website_creator.dimacs_reader import DimacsReader

class TestDimacsReader(unittest.TestCase):
    def setUp(self):
        DIR = "src/tests/testdata_dimacs_graph"
        self.DR = DimacsReader(DIR)

    def test_read_dimacs_graph(self):
        name, number_of_nodes, number_of_edges, sources, licence, short_desc = self.DR.read_dimacs_graph("test_example.dimacs")
        self.assertEqual(name,"dimacsin nimi testi")
        self.assertEqual(number_of_nodes, 5)
        self.assertEqual(number_of_edges, 10)
        self.assertEqual(sources, [('www.dimacs.com', 'www.dimacs.com'), ('www.testi.com', 'www.testi.com')])
        self.assertEqual(licence, "Apache Testi")
        self.assertEqual(short_desc, "short")

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