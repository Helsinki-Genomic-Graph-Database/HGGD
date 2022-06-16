import os
import unittest
from src.dataset_services.dataset_creator import DatasetCreator

class TestGraphDescriptionReadingToDataset(unittest.TestCase):

    def setUp(self):
        self.dir = "src/tests/testdata_with_description_for_graph"
        self.creator = DatasetCreator([self.dir])
        self.dataset = self.creator.get_datasets()[0]
        self.res = self.dataset.get_graph_info()

    def test_dataset_should_have_list_of_tuples_for_graphs(self):
        print(self.res)
        self.assertEqual(len(self.res), 9)

    def test_info_list_should_have_true_for_gfa_for_licence_in_description(self):
        for graph, has_licence, has_sources in self.res:
            if graph == "test_gfa.gfa":
                res = has_licence is not None
        self.assertEqual(res, True)

    def test_info_list_should_have_false_for_dimacs_when_no_description(self):
        for graph, has_licence, has_sources in self.res:
            if graph == "test_dimacs.dimacs":
                res = has_licence
        self.assertEqual(res, None)

    def test_info_list_should_have_false_when_having_no_licence_in_description(self):  
        with open(self.dir+"/test_dimacs_description.json", "w") as file:
            file.write('{"name":"test"}')
        for graph, has_licence, has_sources in self.res:
            if graph == "test_dimacs.dimacs":
                res = has_licence
        os.remove(self.dir+"/test_dimacs_description.json")
        self.assertEqual(res, None)

