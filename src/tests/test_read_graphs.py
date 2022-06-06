"""
import unittest
from src.website_creator.read_graphs import ReadGraphs
from src.entities.dataset import Dataset
from src.entities.graph import Graph


class TestReadGraphs(unittest.TestCase):
    def setUp(self):
        self.dir = "/src/tests/testdata_for_dataset_reader"
        dataset1 = Dataset(True, True, True, self.dir+"/testdata_with_full_description", "name1", "desc1", "desc1", "MIT", "folder", True)
        dataset2 = Dataset(True, True, True, self.dir+"/testdata_with_no_data", "name2", "desc2", "desc2", "GNU", "folder", True)
        dataset_list = [dataset1, dataset2]

"""