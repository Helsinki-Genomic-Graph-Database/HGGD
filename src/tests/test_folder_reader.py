import unittest
from src.file_ui.folder_reader import FolderReader

class TestFolderReaderFullDescription(unittest.TestCase):

    def setUp(self):
        self.folder_reader = FolderReader(["src/tests/testdata_with_full_description"])

    def test_folder_reader_should_give_correct_path(self):
        res = self.folder_reader.get_folder_info()[0][0]
        self.assertEqual(res, "src/tests/testdata_with_full_description")

    def test_folder_reader_should_detect_data(self):
        res = self.folder_reader.get_folder_info()[0][1]
        self.assertEqual(res, True)

    def test_folder_reader_should_detect_description_file(self):
        res = self.folder_reader.get_folder_info()[0][2]
        self.assertEqual(res, True)

    def test_folder_reader_should_detect_name_existing(self):
        res = self.folder_reader.get_folder_info()[0][3]
        self.assertEqual(res, True)

    def test_folder_reader_should_detect_descr_short_existing(self):
        res = self.folder_reader.get_folder_info()[0][4]
        self.assertEqual(res, True)

    def test_folder_reader_should_detect_descr_long_existing(self):
        res = self.folder_reader.get_folder_info()[0][5]
        self.assertEqual(res, True)

class TestFolderReaderReadsMany_folders(unittest.TestCase):

    def setUp(self):
        self.folder_reader = FolderReader(["src/tests/testdata_with_full_description","src/tests/testdata_with_empty_description","src/tests/testdata"])
    
    def test_should_return_list_of_three_infos(self):
        res = self.folder_reader.get_folder_info()
        self.assertEqual(len(res), 3)

class TestFolderReaderWithNoData(unittest.TestCase):

    def setUp(self):
        self.folder_reader = FolderReader(["src/tests/testdata_with_no_data"])

    def test_should_detect_there_are_no_graph_files_in_folder(self):
        res = self.folder_reader.get_folder_info()[0][1]
        self.assertEqual(res, False)

class TestEmptyDesrciptionFile(unittest.TestCase):

    def setUp(self):
        self.folder_reader = FolderReader(["src/tests/testdata_with_empty_description"])

    def test_should_detect_description_file(self):
        res = self.folder_reader.get_folder_info()[0][2]
        self.assertEqual(res, True)

    def test_should_should_detect_no_name(self):
        res = self.folder_reader.get_folder_info()[0][3]
        self.assertEqual(res, False)

class TestNoNameInDescription(unittest.TestCase):

    def setUp(self):
        res = self.folder_reader = FolderReader(["src/tests/testdata_with_description_missing_name"])

    def test_should_detect_description_file(self):
        res = self.folder_reader.get_folder_info()[0][2]
        self.assertEqual(res, True)