import unittest
from src.file_ui.file_utils import read_graph_description
from src.app import get_app
from src.dataset_services.dataset_reader import DatasetReader
from src.dataset_services.dataset_creator import DatasetCreator
from src.tests.mock_spdx import SpdxService

class TestGraphDescrpitionReadsUserDefinedColumns(unittest.TestCase):

    def setUp(self):
        self.dir = "src/tests/testdata_with_example_of_all_graph_formats"
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"descr_short": "s"}')
            desc.close()

        with open(self.dir+"/test_gfa_description.json", "w") as desc:
            desc.write('{"descr_short": "s"}')
            desc.close()

        with open(self.dir+"/test_dimacs_description.json", "w") as desc:
            desc.write('{"descr_short": "s"}')
            desc.close()

    def test_user_defined_columns_should_be_none_when_not_specified(self):
        name, licences, sources, short_desc, user_defined_columns = read_graph_description(self.dir, "test_graph")
        self.assertEqual(user_defined_columns, None)

    def test_user_defined_columns_should_be_read_from_description(self):

        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"descr_short": "s", "user_defined_columns": {"test column strings": ["test string 1", "test string 2"], "test column numbers": [1, 2], "test column strings and numbers": ["test string", 2]}}')
            desc.close()
        name, licences, sources, short_desc, user_defined_columns = read_graph_description(self.dir, "test_graph")
        self.assertEqual(len(user_defined_columns), 3)
        
    def test_user_defined_columns_should_be_none_when_given_in_description_but_empty(self):
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"descr_short": "s", "user_defined_columns": {}}')
            desc.close()

        name, licences, sources, short_desc, user_defined_columns = read_graph_description(self.dir, "test_graph")
        self.assertEqual(user_defined_columns, None)

class TestGraphCreatorAddsUserDefinedColumnsToGraphObject(unittest.TestCase):

    def setUp(self):
        self.data_directory = "src/tests/testdata_with_example_of_all_graph_formats"
        self.spdx_service = SpdxService()
        self.reader = DatasetReader(self.data_directory)
        self.dir_paths = self.reader.get_paths()
        self.creator = DatasetCreator([self.data_directory], self.spdx_service)
        self.dataset = self.creator.get_datasets()[0]

        with open(self.data_directory+"/test_graph_description.json", "w") as desc:
            desc.write('{"descr_short": "s"}')
            desc.close()

    def test_graph_should_have_user_defined_columns_as_none_if_not_defined_in_description(self):
        res = self.dataset.get_list_of_graphs()
        for graph in res:
            if graph.get_names() == "test_graph":
                self.assertEqual(graph.get_user_defined_columns(), [("test column strings", ["test string 1", "test string 2"]), ("test column numbers", [1, 2]), ("test column strings and numbers", ["test string", 2])])
            else:
                self.assertEqual(graph.get_user_defined_columns(), None)

    def test_graph_should_have_user_defined_columns_if_given_in_description(self):
        with open(self.data_directory+"/test_graph_description.json", "w") as desc:
            desc.write('{"descr_short": "s", "user_defined_columns": {"test column strings": ["test string 1", "test string 2"], "test column numbers": [1, 2], "test column strings and numbers": ["test string", 2]}}')
            desc.close()
        self.creator = DatasetCreator([self.data_directory], self.spdx_service)
        self.dataset = self.creator.get_datasets()[0]

        res = self.dataset.get_list_of_graphs()
        for graph in res:
            if graph.get_names() == "test_graph":
                self.assertEqual(len(graph.get_user_defined_columns()), 3)

class TestGraphPageShowsUserDefinedColumns(unittest.TestCase):

    def setUp(self):
        self.dir = "src/tests/mock_datafolder/testdata_with_full_description"
        self.graph = "gt1.kmer15.(736000.738000).V22.E29.cyc128"

    def test_works(self):
        app = get_app().test_client()
        res = app.get("/datasets/testdata_with_full_description/"+self.graph)
        self.assertEqual(res.status_code, 200)

    def test_user_defined_columns_show_on_graph_page(self):
        with open(self.dir+"/"+self.graph+"_description.json", "w") as desc:
            desc.write('{"descr_short": "s", "user_defined_columns": {"test column strings": ["test string 1", "test string 2"], "test column numbers": [1, 2], "test column strings and numbers": ["test string", 2]}}')
            desc.close()

        app = get_app().test_client()
        res = app.get("/datasets/testdata_with_full_description/gt1.kmer15.(736000.738000).V22.E29.cyc128")
        self.assertIn(b"test column strings", res.data)
