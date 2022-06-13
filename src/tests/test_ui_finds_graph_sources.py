import unittest

from src.tests.stub_io import StubIO
from src.dataset_services.dataset_creator import DatasetCreator
from src.data_check.ui import UI

class TestUI(unittest.TestCase):

    def setUp(self):
        creator = DatasetCreator(["src/tests/testdata_with_description_for_graph"])
        dataset_list = creator.get_datasets()
        stubio = StubIO()
        ui = UI(dataset_list, stubio)
        ui.start()
        self.res = stubio.outputs

    def test_folder_should_be_done_with_missing_source_for_graph(self):
        self.assertIn("Folder done.", self.res)

    # def test_ui_should_notify_when_graph_has_no_sources(self):
    #     self.assertIn("")




