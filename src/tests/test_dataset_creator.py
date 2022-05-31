import unittest
from src.helper_functions_for_app import create_dataset

class TestDataSetCreation(unittest.TestCase):


    def test_dataset_should_have_correct_name(self):
        res = create_dataset("src/tests/testdata_with_full_description")
        self.assertEqual(res.name, "testdata with description")

    def test_dataset_should_have_correct_number_of_sources(self):
        res = create_dataset("src/tests/testdata_with_full_description")
        self.assertEqual(len(res.sources), 20)

    def test_dataset_sources_should_have_correct_names(self):
        res = create_dataset("src/tests/testdata_with_full_description")
        assert "GCA_000013265.1_ASM1326v1.fna" in res.sources