import unittest
import os

from src.dataset_services.dataset_creator import DatasetCreator
from src.data_check.spdx_service import SpdxService

class TestSpdxForDatasetCreator(unittest.TestCase):

    def setUp(self):
        self.spdx_service =  SpdxService()
        self.dir = "src/tests/testdata_with_only_three_graphs"
        

    def create_creator(self):
        self.dataset = DatasetCreator([self.dir], self.spdx_service).get_datasets()[0]
        self.dataset_graphs = self.dataset.get_list_of_graphs()

    def tearDown(self):
        if os.path.exists(self.dir+"/test_gfa_description.json"):
            os.remove(self.dir+"/test_gfa_description.json")

        if os.path.exists(self.dir+"/test_graph_description.json"):
            os.remove(self.dir+"/test_graph_description.json")

        if os.path.exists(self.dir+"/test_dimacs_description.json"):
            os.remove(self.dir+"/test_dimacs_description.json")

        if os.path.exists(self.dir+"/description.json"):
            os.remove(self.dir+"/description.json")

    def test_graph_graph_should_have_correct_licence_format_when_licence_in_correct_format_in_description(self):
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"licence": "MIT"}')
        
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_licence()

        self.assertEqual(res, ("MIT", "https://spdx.org/licenses/MIT.html"))

    def test_graph_graph_should_have_correct_licence_format_when_licence_in_incorrect_format_in_description(self):
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"licence": "my own licence"}')
        
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_licence()

        self.assertEqual(res, ("my own licence", None))

    def test_graph_graph_should_have_none_as_licence_when_no_description_given(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_licence()

        self.assertEqual(res, None)

    def test_graph_gets_licence_from_dataset_description_if_has_no_own_licence(self):
        with open(self.dir+"/description.json", "w") as desc:
            desc.write('{"licence": "MIT"}')
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_licence()

        self.assertEqual(res, ("MIT", "https://spdx.org/licenses/MIT.html"))

    def test_graph_keeps_its_own_licence_even_if_dataset_description_has_licence(self):
        with open(self.dir+"/description.json", "w") as desc:
            desc.write('{"licence": "my own licence"}')
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"licence": "MIT"}')
        
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_licence()

        self.assertEqual(res, ("MIT", "https://spdx.org/licenses/MIT.html"))