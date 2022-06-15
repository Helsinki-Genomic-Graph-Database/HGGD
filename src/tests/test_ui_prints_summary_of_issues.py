import unittest
import os
import time
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

class TestUIGraphLicencesWithLiceneGivenInUI(unittest.TestCase):

    def setUp(self):
        creator = DatasetCreator(["src/tests/testdata"])
        self.dataset_list = creator.get_datasets()

    def tearDown(self):
        os.remove("src/tests/testdata/description.json")
        os.remove("src/tests/testdata/log.txt")

    def test_ui_should_not_notify_if_licence_is_added_in_ui(self):
        stubio = StubIO(["test name", "short", "long", "licence"])
        ui = UI(self.dataset_list, stubio)
        ui.start()
        res = stubio.outputs
        self.assertNotIn("\033[1;33;40mDataset 'test name' in folder 'testdata has 5 graph(s) with no licence given.\033[0;37;40m", res)

    def test_ui_should_notify_if_no_licence_given_in_ui(self):
        stubio = StubIO(["test name", "short", "long", ""])
        ui = UI(self.dataset_list, stubio)
        ui.start()
        res = stubio.outputs
        self.assertIn("\033[1;33;40mDataset 'test name' in folder 'testdata' has 5 graph(s) with no licence given.\033[0;37;40m", res)

    def test_ui_should_tell_there_are_two_issues_when_long_descr_and_licence_not_given_when_graphs_dont_have_licences(self):
        stubio = StubIO(["test name", "short", "", ""])
        ui = UI(self.dataset_list, stubio)
        ui.start()
        res = stubio.outputs
        self.assertIn("\033[1;33;40m2 issue(s) found in datasets\033[0;37;40m", res)

class TestUINotificationsWithLogOrNot(unittest.TestCase):

    def setUp(self):
        self.dir = "src/tests/testdata_with_no_licences_for_graphs_and_no_log"
        #folder has on of each graph format, licence.json and test_gfa_descrpition.json
        creator = DatasetCreator([self.dir])
        self.dataset_list = creator.get_datasets()

    def test_ui_should_notify_correctly_with_no_log_in_folder(self):
        stubio = StubIO(["test name", "short", "long", "licence"])
        ui = UI(self.dataset_list, stubio)
        ui.start()
        res = stubio.outputs
        os.remove(self.dir+"/log.txt")
        self.assertIn("\033[1;33;40m1 issue(s) found in datasets\033[0;37;40m", res)

    def test_ui_should_notify_correctly_with_log_in_folder(self):
        with open(self.dir+"/log.txt", "w") as file:
            file.write("test")
        time.sleep(0.05)
        stubio = StubIO(["test name", "short", "long", "licence"])
        ui = UI(self.dataset_list, stubio)
        ui.start()
        res = stubio.outputs
        os.remove(self.dir+"/log.txt")
        self.assertIn("\033[1;33;40m1 issue(s) found in datasets\033[0;37;40m", res)

    def test_ui_should_notify_correctly_with_no_log_and_no_description(self):
        os.rename(self.dir+"/description.json", self.dir+"/!description.json")
        creator = DatasetCreator([self.dir])
        self.dataset_list = creator.get_datasets()
        stubio = StubIO(["test name", "short", "long", "licence"])
        ui = UI(self.dataset_list, stubio)
        ui.start()
        res = stubio.outputs
        os.remove(self.dir+"/log.txt")
        os.rename(self.dir+"/!description.json", self.dir+"/description.json")
        self.assertIn("\033[1;33;40m1 issue(s) found in datasets\033[0;37;40m", res)

    def test_ui_should_notify_correctly_with_no_description_and_no_optional_info_in_description_file(self):
        os.rename(self.dir+"/description.json", self.dir+"/!description.json")
        creator = DatasetCreator([self.dir])
        self.dataset_list = creator.get_datasets()
        stubio = StubIO(["test name", "short", "", ""])
        ui = UI(self.dataset_list, stubio)
        ui.start()
        res = stubio.outputs
        os.remove(self.dir+"/log.txt")
        os.rename(self.dir+"/!description.json", self.dir+"/description.json")
        self.assertIn("\033[1;33;40m3 issue(s) found in datasets\033[0;37;40m", res)

    def test_ui_should_not_notify_issues_if_here_are_no_issues(self):
        os.rename(self.dir+"/test_dimacs.dimacs", self.dir+"/test_dimacs.!dimacs")
        creator = DatasetCreator([self.dir])
        self.dataset_list = creator.get_datasets()
        stubio = StubIO(["test name", "short", "long", "licence"])
        ui = UI(self.dataset_list, stubio)
        ui.start()
        res = stubio.outputs
        os.remove(self.dir+"/log.txt")
        os.rename(self.dir+"/test_dimacs.!dimacs", self.dir+"/test_dimacs.dimacs")
        print(res)
        self.assertEqual(len(res), 13)

    def test_ui_should_ask_if_issues_should_be_listed(self):
        os.rename(self.dir+"/description.json", self.dir+"/!description.json")
        creator = DatasetCreator([self.dir])
        self.dataset_list = creator.get_datasets()
        stubio = StubIO(["test name", "short", "", ""])
        ui = UI(self.dataset_list, stubio)
        ui.start()
        res = stubio.outputs
        os.remove(self.dir+"/log.txt")
        os.rename(self.dir+"/!description.json", self.dir+"/description.json")
        self.assertIn("\033[1;33;40mShow issues in detail?(y/n)\033[0;37;40m", res)

    def test_ui_should_list_details_of_issues_if_asked(self):
        os.rename(self.dir+"/description.json", self.dir+"/!description.json")
        creator = DatasetCreator([self.dir])
        self.dataset_list = creator.get_datasets()
        stubio = StubIO(["test name", "short", "", ""])
        ui = UI(self.dataset_list, stubio)
        ui.start()
        res = stubio.outputs
        os.remove(self.dir+"/log.txt")
        os.rename(self.dir+"/!description.json", self.dir+"/description.json")
        self.assertIn(f"\033[1;33;40m'test name' in folder 'testdata_with_no_licences_for_graphs_and_no_log' has no long description\033[0;37;40m", res)

    def test_ui_should_not_list_details_of_issues_if_not_asked(self):
        os.rename(self.dir+"/description.json", self.dir+"/!description.json")
        creator = DatasetCreator([self.dir])
        self.dataset_list = creator.get_datasets()
        stubio = StubIO(["test name", "short", "", "", "n"])
        ui = UI(self.dataset_list, stubio)
        ui.start()
        res = stubio.outputs
        os.remove(self.dir+"/log.txt")
        os.rename(self.dir+"/!description.json", self.dir+"/description.json")
        self.assertNotIn(f"\033[1;33;40m'test name' in folder 'testdata_with_no_licences_for_graphs_and_no_log' has no long description\033[0;37;40m", res)
