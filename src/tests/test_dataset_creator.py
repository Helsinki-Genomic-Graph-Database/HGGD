import unittest
import os
from time import sleep
from src.dataset_services.dataset_creator import DatasetCreator
from src.tests.mock_spdx import SpdxService


class TestDataSetCreator(unittest.TestCase):

    def setUp(self):
        testdatadir = "src/tests/testdata"
        self.full_descr = testdatadir+"_with_full_description"
        self.no_name_descr = testdatadir+"_with_description_missing_name"
        self.empty_descr = testdatadir+"_with_empty_description"
        self.no_data = testdatadir+"_with_no_data"
        self.no_descr = testdatadir
        self.no_log = testdatadir+"_with_no_log"
        self.with_user_defined_columns = testdatadir+"_with_user_defined_columns"
        self.spdx_service = SpdxService()
        
    def test_given_folders_should_return_list_of_5_dataset_objects(self):
        creator = DatasetCreator([self.full_descr, self.no_name_descr, self.empty_descr, self.no_data, self.no_descr], self.spdx_service)
        res = creator.get_datasets()
        self.assertEqual(len(res), 5)

    def test_creator_should_detect_description_existing(self):
        creator = DatasetCreator([self.full_descr], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_description_file_exists(),True)

    def test_creator_should_detect_description_missing(self):
        creator = DatasetCreator([self.no_descr], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_description_file_exists(),False)

    def test_creator_should_detect_data_exisiting(self):
        creator = DatasetCreator([self.full_descr], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_data_exists(), True)

    def test_creator_should_detect_data_missing(self):
        creator = DatasetCreator([self.no_data], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_data_exists(), False)

    def test_dataset_should_have_correct_path(self):
        creator = DatasetCreator([self.full_descr], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_path(), self.full_descr)

    def test_creator_should_detect_name(self):
        creator = DatasetCreator([self.full_descr], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_name(), "testdata with description")

    def test_creator_should_detect_no_name_in_description(self):
        creator = DatasetCreator([self.no_name_descr], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_name(), None)

    def test_creator_should_give_name_as_none_with_no_description_file(self):
        creator = DatasetCreator([self.no_descr], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_name(), None)

    def test_creator_should_detect_descr_short_in_description(self):
        creator = DatasetCreator([self.full_descr], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_descr_short(), "with full description")

    def test_creator_should_detect_descr_long_in_description(self):
        creator = DatasetCreator([self.full_descr], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_descr_long(), "testing data")
        
    def test_creator_should_detect_licence_in_description(self):
        creator = DatasetCreator([self.full_descr], self.spdx_service)
        res = creator.get_datasets()[0]
        licence_tuple = res.get_licence()[0]
        licence = licence_tuple[0]
        self.assertEqual(licence, "MIT")

    def test_creator_should_find_folder_name(self):
        creator = DatasetCreator([self.full_descr], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_folder_name(), "testdata_with_full_description")

    def test_creator_should_detect_no_files_updated_after_log(self):
        creator = DatasetCreator([self.no_log], self.spdx_service)
        with open(self.no_log+"/log.txt", "w") as log:
            log.write("test")
        res = creator.get_datasets()[0]
        os.remove(self.no_log+"/log.txt")
        self.assertEqual(res.get_show_on_website(), True)

    def test_creator_should_detect_no_log(self):
        creator = DatasetCreator([self.no_log], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_show_on_website(), False)

    def test_creator_should_detect_file_added_after_log(self):
        creator = DatasetCreator([self.no_log], self.spdx_service)
        with open(self.no_log+"/log.txt", "w") as log:
            log.write("test")
        sleep(0.05)
        with open(self.no_log+"/test.graph", "w") as test:
            test.write("test")
        res = creator.get_datasets()[0]
        os.remove(self.no_log+"/log.txt")
        os.remove(self.no_log+"/test.graph")
        self.assertEqual(res.get_show_on_website(), False)

    def test_creator_should_prevent_no_data_set_from_displaying(self):
        creator = DatasetCreator([self.no_data], self.spdx_service)
        with open(self.no_data+"/log.txt", "w") as log:
            log.write("test")
        res = creator.get_datasets()[0]
        self.assertEqual(res.get_show_on_website(), False)

    def test_creator_should_read_a_list_from_user_defined_strings(self):
        creator = DatasetCreator([self.with_user_defined_columns], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertEqual(len(res.get_user_defined_columns()), 3)

    def test_each_column_in_user_defined_columns_should_be_a_tuple(self):
        creator = DatasetCreator([self.with_user_defined_columns], self.spdx_service)
        res = creator.get_datasets()[0]
        self.assertIsInstance(res.get_user_defined_columns()[0], tuple)

    def test_values_in_user_defined_columns_should_be_correct(self):
        creator = DatasetCreator([self.with_user_defined_columns], self.spdx_service)
        res = creator.get_datasets()[0].get_user_defined_columns()[2][1]
        self.assertIn("test string", res)
        self.assertIn(2, res)

    def test_licence_should_be_list(self):
        creator = DatasetCreator([self.no_descr], self.spdx_service)
        res = creator.get_datasets()[0].get_licence()
        self.assertIsInstance(res, list)

    def test_licence_list_should_be_empty_with_no_licences(self):
        creator = DatasetCreator([self.no_descr], self.spdx_service)
        res = creator.get_datasets()[0].get_licence()
        self.assertEqual(len(res), 0)

    def test_licenses_should_be_added_to_list(self):
        creator = DatasetCreator([self.full_descr], self.spdx_service)
        res = creator.get_datasets()[0].get_licence()
        self.assertEqual(len(res), 1)

    def test_sources_exists_for_full_desc(self):
        creator = DatasetCreator([self.full_descr], self.spdx_service)
        res = creator.get_datasets()[0].get_dataset_source()
        self.assertIn(("test source", "test source"), res)
