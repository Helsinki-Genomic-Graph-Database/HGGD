import unittest
import os
from datetime import datetime
from src.file_ui.folder_reader import FolderReader
from src.text_ui.ui import UI
from src.tests.stub_io import StubIO
from src.file_ui.file_utils import check_log_update_after_file_modified

class TestLogCreationWithNoLogInFolder(unittest.TestCase):

    def setUp(self):
        self.DIR = "src/tests/testdata_with_no_log"
        self.folder_reader = FolderReader([self.DIR])

    def tearDown(self):
        if os.path.exists(f"{self.DIR}/log.txt"):
            os.remove(f"{self.DIR}/log.txt")
        if os.path.exists(f"{self.DIR}/test.graph"):
            os.remove(f"{self.DIR}/test.graph")

    def test_should_notice_no_log(self):
        info_list = self.folder_reader.get_folder_info()
        res = info_list[0][7]
        self.assertEqual(res, False)

    def test_folder_reader_should_create_log_to_folder(self):
        self.folder_reader.run()
        res = os.path.exists(f"{self.DIR}/log.txt")
        self.assertEqual(res, True)

    def test_UI_should_update_log_when_folder_is_done(self):
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(self.folder_reader, io)
        ui.start()
        with open(f"{self.DIR}/log.txt") as log:
            line = log.readline()
        logstamp = datetime.now().isoformat(" ", "seconds")
        self.assertEqual(line, f"ui run on: {logstamp}")

    def test_should_notice_file_modified_after_log_update(self):
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(self.folder_reader, io)
        ui.start()
        with open(f"{self.DIR}/test.graph", "w") as f:
            f.write("test")
        with open(f"{self.DIR}/log.txt") as log:
            line = log.readline()
        res = check_log_update_after_file_modified(f"{self.DIR}/test.graph", line)
        self.assertEqual(res, False)
        
class TestLogCreationWithLogInFolder(unittest.TestCase):

    def setUp(self):
        self.DIR = "src/tests/testdata_with_log"
        self.folder_reader = FolderReader([self.DIR])

    def test_should_notice_log_updated_after_file_modified(self):
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(self.folder_reader, io)
        ui.start()
        with open(f"{self.DIR}/log.txt") as log:
            line = log.readline()
        res = check_log_update_after_file_modified(f"{self.DIR}/gt20.kmer15.(102000.104000).V75.E104.cyc1000.graph", line)
        self.assertEqual(res, True)