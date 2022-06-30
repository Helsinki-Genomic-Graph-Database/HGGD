import unittest
import os
from src.dataset_services.dataset_creator import DatasetCreator
from src.tests.mock_spdx import SpdxService
from src.data_check.ui import UI
from src.tests.stub_io import StubIO

class TestUiPrintsSummaryOfIssues(unittest.TestCase):
    def setUp(self):
        self.spdx_service = SpdxService()
        self.dir = "src/tests/testdata_with_only_one_dataset/testdata_with_only_three_graphs"

    def create_creator(self):
        self.dataset = DatasetCreator([self.dir], self.spdx_service).get_datasets()
        self.dataset[0].set_show_on_website(False)
        self.dataset_graphs = self.dataset[0].get_list_of_graphs()

    def tearDown(self):
        if os.path.exists(self.dir+"/test_gfa_description.json"):
            os.remove(self.dir+"/test_gfa_description.json")

        if os.path.exists(self.dir+"/test_graph_description.json"):
            os.remove(self.dir+"/test_graph_description.json")

        if os.path.exists(self.dir+"/test_dimacs_description.json"):
            os.remove(self.dir+"/test_dimacs_description.json")

        if os.path.exists(self.dir+"/description.json"):
            os.remove(self.dir+"/description.json")

        if os.path.exists(self.dir+"/log.txt"):
            os.remove(self.dir+"/log.txt")

    def test_if_dataset_nor_graph_have_description_files_and_licence_not_given_in_ui_shows_issues(self):
        self.create_creator()
        inputs = ["test_name", "test_short", "", "", "gfa_short", "graph_short", "dimacs_short", "y"] # name, short desc, long desc, licence, gfa desc, graph desc, dimacs desc, show details?
        io = StubIO(inputs)
        ui = UI(self.dataset, io, self.spdx_service)
        ui.start()
        final_string_should_be = "\033[1;33;40mDataset 'test_name' in folder 'testdata_with_only_three_graphs' has \
3 graph(s) with no licence given.\033[0;37;40m"
        self.assertEqual(io.outputs[-1], final_string_should_be)

    def test_if_dataset_nor_graph_have_description_files_but_spdx_licence_is_given_in_ui_doesnt_show_issues(self):
        self.create_creator()
        inputs = ["test_name", "test_short", "long desc", "MIT", "gfa_short", "graph_short", "dimacs_short", "y"] # name, short desc, long desc, licence, gfa desc, graph desc, dimacs desc, show details?
        io = StubIO(inputs)
        ui = UI(self.dataset, io, self.spdx_service)
        ui.start()
        final_string_should_be = "Folder done."
        self.assertEqual(io.outputs[-1], final_string_should_be)

    def test_if_dataset_nor_graph_have_description_files_but_non_spdx_licence_is_given_in_ui_shows_issues(self):
        self.create_creator()
        inputs = ["test_name", "test_short", "", "Apache", "gfa_short", "graph_short", "dimacs_short", "y"] # name, short desc, long desc, licence, gfa desc, graph desc, dimacs desc, show details?
        io = StubIO(inputs)
        ui = UI(self.dataset, io, self.spdx_service)
        ui.start()
        for o in io.outputs:
            print(o)
        final_string_should_be = "\033[1;33;40mDataset 'test_name' in folder 'testdata_with_only_three_graphs' has a licence that is not in SPDX format.\033[0;37;40m"
        self.assertEqual(io.outputs[28], final_string_should_be)

    def test_if_dataset_description_has_spdx_licence_but_graph_doesnt_have_licence_shows_no_issues(self):
        with open(self.dir+"/description.json", "w") as desc:
            desc.write('{"licence": "MIT"}')
        self.create_creator()
        inputs = ["test_name", "test_short", "long desc", "gfa_short", "graph_short", "dimacs_short", "y"] # name, short desc, long desc, licence, gfa desc, graph desc, dimacs desc, show details?
        io = StubIO(inputs)
        ui = UI(self.dataset, io, self.spdx_service)
        ui.start()
        final_string_should_be = "Folder done."
        self.assertEqual(io.outputs[-1], final_string_should_be)

    def test_if_dataset_description_has_spdx_licence_but_graph_has_non_spdx_licence_shows_issues(self):
        with open(self.dir+"/description.json", "w") as desc:
            desc.write('{"licence": "MIT"}')
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"licence": "non-spdx"}')
        self.create_creator()
        inputs = ["test_name", "test_short", "long desc", "gfa_short", "graph_short", "dimacs_short", "y"] # name, short desc, long desc, licence, gfa desc, graph desc, dimacs desc, show details?
        io = StubIO(inputs)
        ui = UI(self.dataset, io, self.spdx_service)
        ui.start()
        final_string_should_be = "\033[1;33;40mDataset 'test_name' in folder 'testdata_with_only_three_graphs' has a licence that is not in SPDX format.\033[0;37;40m"
        self.assertEqual(io.outputs[25], final_string_should_be)
        pass

    def test_if_all_graphs_have_licence_in_description_but_dataset_doesnt_shows_no_issues(self):
        with open(self.dir+"/test_gfa_description.json", "w") as desc:
            desc.write('{"licence": "MIT"}')
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"licence": "MIT"}')
        with open(self.dir+"/test_dimacs_description.json", "w") as desc:
            desc.write('{"licence": "MIT"}')
        self.create_creator()
        inputs = ["test_name", "test_short", "long desc", "", "gfa_short", "graph_short", "dimacs_short", "y"] # name, short desc, long desc, licence, gfa desc, graph desc, dimacs desc, show details?
        io = StubIO(inputs)
        ui = UI(self.dataset, io, self.spdx_service)
        ui.start()
        final_string_should_be = "Folder done."
        self.assertEqual(io.outputs[-1], final_string_should_be)

    def test_if_dataset_has_non_spdx_licence_but_some_graphs_have_spdx_licence_shows_issues(self):
        with open(self.dir+"/description.json", "w") as desc:
            desc.write('{"licence": "non-spdx"}')
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"licence": "MIT"}')
        self.create_creator()
        inputs = ["test_name", "test_short", "long desc", "gfa_short", "graph_short", "dimacs_short", "y"] # name, short desc, long desc, licence, gfa desc, graph desc, dimacs desc, show details?
        io = StubIO(inputs)
        ui = UI(self.dataset, io, self.spdx_service)
        ui.start()
        for o in io.outputs:
            print(o)
        final_string_should_be = "\033[1;33;40mDataset 'test_name' in folder 'testdata_with_only_three_graphs' has a licence that is not in SPDX format.\033[0;37;40m"
        self.assertEqual(io.outputs[25], final_string_should_be)

    def test_if_dataset_and_graphs_have_non_spdx_licences_lists_them_correctly(self):
        with open(self.dir+"/description.json", "w") as desc:
            desc.write('{"licence": "dataset non-spdx"}')
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"licence": "graph non-spdx"}')
        with open(self.dir+"/test_gfa_description.json", "w") as desc:
            desc.write('{"licence": "gfa non-spdx"}')
        with open(self.dir+"/test_dimacs_description.json", "w") as desc:
            desc.write('{"licence": "dimacs non-spdx"}')
        self.create_creator()
        inputs = ["test_name", "test_short", "long desc", "gfa_short", "graph_short", "dimacs_short", "y"] # name, short desc, long desc, licence, gfa desc, graph desc, dimacs desc, show details?
        io = StubIO(inputs)
        ui = UI(self.dataset, io, self.spdx_service)
        ui.start()
        output_set = set()
        for output in io.outputs:
            output_set.add(output)
        licence_list = "These licences are not in SPDX format: "
        licence_dimacs = "dimacs non-spdx"
        licence_dataset = "dataset non-spdx"
        licence_graph = "graph non-spdx"
        licence_gfa = "gfa non-spdx"
        self.assertEqual(licence_list, io.outputs[26])
        self.assertIn(licence_dimacs, output_set)
        self.assertIn(licence_dataset, output_set)
        self.assertIn(licence_graph, output_set)
        self.assertIn(licence_gfa, output_set)

    def test_if_graph_doesnt_have_source_shows_issue(self):
        pass

    def test_if_graph_has_source_doesnt_show_issues(self):
        pass

    def test_if_dataset_has_long_desc_in_jsonfile_doesnt_show_issues(self):
        pass

    def test_if_dataset_doesnt_have_long_desc_in_jsonfile_and_not_given_in_ui_shows_issues(self):
        pass

    def test_if_dataset_doesnt_have_long_desc_in_jsonfile_but_its_given_in_ui_doesnt_show_issues(self):
        pass
