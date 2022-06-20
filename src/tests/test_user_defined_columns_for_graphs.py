import unittest
import os
from src.file_ui.file_utils import read_graph_description

class TestGraphDescrpitionReadsUserDefinedColumns(unittest.TestCase):

    def setUp(self):
        self.dir = "src/tests/testdata_with_example_of_all_graph_formats"