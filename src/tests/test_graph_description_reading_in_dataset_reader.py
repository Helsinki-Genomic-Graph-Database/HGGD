import unittest
from src.dataset_services.dataset_creator import DatasetCreator

class TestGraphDescriptionReadingToDataset(unittest.TestCase):

    def setUp(self):
        dir = "src/tests/testdata_with_description_for_graph"
        self.creator = DatasetCreator([dir])
        self.dataset = self.creator.get_datasets()[0]

    def test_dataset_should_have_list_of_tuples_for_graphs(self):
        res = self.dataset.get_graph_info()
        self.assertEqual(len(res), 7)