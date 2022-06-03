import unittest
from src.dataset_services.dataset_creator import DatasetCreator


class TestDataSetCreator(unittest.TestCase):

    def setUp(self):
        testdatadir = "src/tests/testdata"
        self.full_descr = testdatadir+"_with_full_description"
        self.no_name_descr = testdatadir+"_with_description_missing_name"
        self.empty_descr = testdatadir+"_with_empty_description"
        self.no_data = testdatadir+"_with_no_data"
        self.no_descr = testdatadir
        
    def test_given_folders_should_return_list_of_5_datset_objects(self):
        creator = DatasetCreator([self.full_descr, self.no_name_descr, self.empty_descr, self.no_data, self.no_descr])
        res = creator.get_datasets()
        self.assertEqual(len(res), 5)

    def test_creator_should_detect_description_existing(self):
        creator = DatasetCreator([self.full_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_description_file_exists(),True)

    def test_creator_should_detect_description_missing(self):
        creator = DatasetCreator([self.no_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_description_file_exists(),False)

    def test_creator_should_detect_data_exisiting(self):
        creator = DatasetCreator([self.full_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_data_exists(), True)

    def test_creator_should_detect_data_missing(self):
        creator = DatasetCreator([self.no_data])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_data_exists(), False)

    def test_creator_should_detect_licence_file_existing(self):
        creator = DatasetCreator([self.full_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_licence_file_exists(), True)

    def test_creator_should_detect_licence_file_missing(self):
        creator = DatasetCreator([self.no_name_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_licence_file_exists(), False)

    def test_dataset_should_have_correct_path(self):
        creator = DatasetCreator([self.full_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_path(), self.full_descr)

    def test_creator_should_detect_name(self):
        creator = DatasetCreator([self.full_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_name(), "testdata with description")

    def test_creator_should_detect_no_name_in_description(self):
        creator = DatasetCreator([self.no_name_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_name(), None)

    def test_creator_should_give_name_as_none_with_no_description_file(self):
        creator = DatasetCreator([self.no_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_name(), None)

    def test_creator_should_detect_descr_short_in_description(self):
        creator = DatasetCreator([self.full_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_descr_short(), "with full description")

    def test_creator_should_detect_descr_long_in_description(self):
        creator = DatasetCreator([self.full_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_descr_long(), "testing data")
        
    def test_creator_should_detect_licence_in_description(self):
        creator = DatasetCreator([self.full_descr])
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_licence(), "test_licence")