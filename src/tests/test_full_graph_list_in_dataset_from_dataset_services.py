import unittest
import os
from src.dataset_services.dataset_creator import DatasetCreator
from src.tests.mock_spdx import SpdxService

class TestDataSetCreatorGivesFullGraphLists(unittest.TestCase):

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


    def test_datasets_have_graph_list_with_graph_for_each_file(self):
        self.create_creator()
        self.assertEqual(len(self.dataset_graphs), 3)

    def test_if_graph_has_no_description_file_it_still_has_a_name_from_file_name(self):
        self.create_creator()
        res = False
        for graph in self.dataset_graphs:
            print(graph.get_names())
            if graph.get_names() == "test_gfa":
                res = True

        self.assertEqual(res, True)

    def test_dataset_graphs_get_name_from_own_description_file_if_given(self):
        with open(self.dir+"/test_gfa_description.json", "w") as desc:
            desc.write('{"name": "Test GFA"}')
        res = False
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "Test GFA":
                res = True

        self.assertEqual(res, True)

    def test_dataset_dot_graphs_have_correct_amount_of_nodes(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_nodes()
        self.assertEqual(res, 21)

    def test_dataset_gfa_graphs_have_correct_number_of_nodes(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_gfa":
                res = graph.get_nodes()
        self.assertEqual(res, 6)

    def test_dataset_dimacs_graphs_have_correct_number_of_nodes(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_dimacs":
                res = graph.get_nodes()
        self.assertEqual(res, 5)

    def test_dataset_dot_graphs_have_correct_amount_of_edges(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_edges()
        self.assertEqual(res, 27)

    def test_dataset_gfa_graphs_have_correct_amount_of_edges(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_gfa":
                res = graph.get_edges()
        self.assertEqual(res, 4)

    def test_dataset_dimacs_graphs_have_correct_amount_of_edges(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_dimacs":
                res = graph.get_edges()
        self.assertEqual(res, 10)

    def test_dot_graph_sources_are_list_of_tuples(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_sources()[0]
        self.assertIsInstance(res,tuple)
        
    def test_gfa_sources_are_empty_list_if_dont_exist(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_gfa":
                res = graph.get_sources()
        self.assertEqual(res, [])

    def test_dimacs_sources_are_empty_list_if_dont_exist(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_dimacs":
                res = graph.get_sources()
        self.assertEqual(res, [])

    def test_dot_graph_sources_are_overwritten_from_description_file(self):
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"sources": ["test source 1", "test source 2"]}')
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_sources()
        self.assertEqual(len(res), 2)

    def test_gfa_gets_sources_from_description_if_given(self):
        with open(self.dir+"/test_gfa_description.json", "w") as desc:
            desc.write('{"sources": ["test source 1", "test source 2"]}')
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_gfa":
                res = graph.get_sources()
        self.assertEqual(len(res), 2)

    def test_dimacs_gets_sources_from_description_if_given(self):
        with open(self.dir+"/test_dimacs_description.json", "w") as desc:
            desc.write('{"sources": ["test source 1", "test source 2"]}')
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_dimacs":
                res = graph.get_sources()
        
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0][0], res[0][1])

    def test_sources_for_dot_graphs_are_converted_to_links_if_in_fna_format(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_sources()[0]
        
        self.assertNotEqual(res[0], res[1])

    def test_dot_graph_has_graph_as_file_format(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_file_format()
        self.assertEqual(res, "graph")

    def test_dimacs_has_dimacs_as_file_format(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_dimacs":
                res = graph.get_file_format()
        self.assertEqual(res, "dimacs")

    def test_dot_graph_has_correct_filename(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_file_name()
        self.assertEqual(res, "test_graph.graph")

    def test_dimacs_has_correct_filename(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_dimacs":
                res = graph.get_file_name()
        self.assertEqual(res, "test_dimacs.dimacs")

    def test_dot_graph_has_short_desc_if_given_in_description(self):
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"descr_short": "test desc 1"}')
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_short_desc()
        self.assertEqual(res, "test desc 1")

    def test_dimacs_has_short_desc_if_given_in_description(self):
        with open(self.dir+"/test_dimacs_description.json", "w") as desc:
            desc.write('{"descr_short": "test desc 1"}')
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_dimacs":
                res = graph.get_short_desc()
        self.assertEqual(res, "test desc 1")

    def test_short_descr_is_none_if_not_given(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_dimacs":
                res = graph.get_short_desc()
        self.assertEqual(res, None)

    def test_dot_graph_has_user_defined_columns_if_given_in_description(self):
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"user_defined_columns": {"test 1": [1, 2]}}')
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_user_defined_columns()
        self.assertEqual(res, [("test 1", [1, 2])])

    def test_dimacs_as_user_defined_columns_if_given_in_description(self):
        with open(self.dir+"/test_dimacs_description.json", "w") as desc:
            desc.write('{"user_defined_columns": {"test 1": [1, 2]}}')
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_dimacs":
                res = graph.get_user_defined_columns()
        self.assertEqual(res, [("test 1", [1, 2])])

    def test_user_defined_columns_is_none_if_not_given(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_dimacs":
                res = graph.get_user_defined_columns()
        self.assertEqual(res, None)

    def test_dot_graph_has_description_file_exists_true_if_has_description_file(self):
        with open(self.dir+"/test_graph_description.json", "w") as desc:
            desc.write('{"user_defined_columns": {"test 1": [1, 2]}}')
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_description_file_exists()
        self.assertEqual(res, True)

    def test_dimacs_has_description_file_exists_true_if_has_description_file(self):
        with open(self.dir+"/test_dimacs_description.json", "w") as desc:
            desc.write('{"user_defined_columns": {"test 1": [1, 2]}}')
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_dimacs":
                res = graph.get_description_file_exists()
        self.assertEqual(res, True)

    def test_dot_graph_has_description_file_exists_false_if_no_description_file(self):
        self.create_creator()
        for graph in self.dataset_graphs:
            if graph.get_names() == "test_graph":
                res = graph.get_description_file_exists()
        self.assertEqual(res, False)

    


    