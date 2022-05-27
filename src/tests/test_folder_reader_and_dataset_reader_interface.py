import unittest
from src.file_ui.dataset_reader import DatasetReader
from src.file_ui.folder_reader import FolderReader
class TestInterface(unittest.TestCase):

    def setUp(self):
        DIR = "src/tests/testdata_for_dataset_reader"
        self.dataset_reader = DatasetReader(DIR)
        self.folder_reader = FolderReader(self.dataset_reader.get_paths())

    def test_folder_reader_returns_info_for_two_folders(self):
        res = self.folder_reader.get_folder_info()
        self.assertEqual(len(res), 2)

    def test_folder_reader_finds_correct_path(self):
        res = False
        infos = self.folder_reader.get_folder_info()
        for info in infos:
            if info[0] == "src/tests/testdata_for_dataset_reader/testdata_with_no_data":
                res = True

        self.assertEqual(res, True)
