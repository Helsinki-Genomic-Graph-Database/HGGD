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

    def test_ui_should_notify_when_graph_has_no_sources(self):
        self.assertIn("\033[1;33;40mDataset 'testdata with description' in folder 'testdata_with_description_for_graph' has 1 graph(s) with missing source files.\033[0;37;40m", self.res)


class TestUIGraphLicences(unittest.TestCase):

    def setUp(self):
        creator = DatasetCreator(["src/tests/testdata_with_no_licence_for_all_graphs"])
        dataset_list = creator.get_datasets()
        stubio = StubIO([""])
        ui = UI(dataset_list, stubio)
        ui.start()
        self.res = stubio.outputs

    def test_folder_should_be_done_with_graphs_missing_licence(self):
        self.assertIn("Folder done.", self.res)

    def test_ui_should_notify_when_graphs_have_no_licence(self):
        self.assertIn("\033[1;33;40mDataset 'testdata with description' in folder 'testdata_with_no_licence_for_all_graphs' has 7 graph(s) with no licence given.\033[0;37;40m", self.res)