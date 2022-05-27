import unittest
from src.calculator import Calculator
from src.dataset import Dataset
from src.graph import Graph

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()
        self.graph_list = [Graph("name1", 11, 12), Graph("name2", 13, 14), Graph("name3", 15, 16)]
        self.dataset = Dataset("name", self.graph_list)

    def test_get_no_nodes_and_edges(self):
        nodes, edges = self.calculator.get_no_nodes_and_edges(self.dataset)
        self.assertEqual(39, nodes)
        self.assertEqual(42, edges)

    def test_calculate_statistics(self):
        graphs_total, avg_nodes, avg_edges = self.calculator.calculate_statistics(self.dataset)
        self.assertEqual(3, graphs_total)
        self.assertEqual(13, avg_nodes)
        self.assertEqual(14, avg_edges)
