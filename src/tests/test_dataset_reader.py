import unittest
from src.dataset_services.dataset_reader import DatasetReader

class TestDatasetReader(unittest.TestCase):

    def setUp(self):
        DIR = "src/tests/testdata_for_dataset_reader"
        self.dataset_reader = DatasetReader(DIR)

    def test_dataset_reader_should_return_list_of_three_paths(self):
        res = self.dataset_reader.get_paths()
        self.assertEqual(len(res), 2)

    def test_list_should_include_path_to_test2_folder(self):
        res = self.dataset_reader.get_paths()
        assert "src/tests/testdata_for_dataset_reader/testdata_with_no_data" in res
