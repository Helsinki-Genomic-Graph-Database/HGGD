import unittest
from src.file_ui.folder_reader import FolderReader

class TestLogCreationWithNoLogInFolder(unittest.TestCase):

    def setUp(self):
        DIR = "src/tests/testdata_with_no_log"
        self.folder_reader = FolderReader([DIR])

    def test_should_notice_no_log(self):
        info_list = self.folder_reader.get_folder_info()
        res = info_list[0][7]
        self.assertEqual(res, False)

