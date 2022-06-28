
import unittest
from src.website_creator.read_graphs import ReadGraphs
from src.entities.dataset import Dataset


class TestReadGraphs(unittest.TestCase):
    def setUp(self):
        self.dir = "./src/tests/testdata_for_dataset_reader"
        dataset1 = Dataset(True, True, True, self.dir+"/testdata_with_full_description", "name1", "desc1", "desc1", "MIT", True, "testdata_with_full_description")
        dataset2 = Dataset(True, True, True, self.dir+"/testdata_with_no_data", "name2", "desc2", "desc2", "GNU", True, "testdata_with_no_data")
        dataset_list = [dataset1, dataset2]
        self.readgraphs = ReadGraphs(dataset_list)
        self.readgraphs.run()
        self.updated_list = self.readgraphs.get_dataset_list_with_graphs()
    
    def test_returns_list(self):
        self.assertIsInstance(self.updated_list, list)

    def test_graphs_list_length(self):
        self.assertEqual(len(self.updated_list[0].get_list_of_graphs()), 5)
        self.assertEqual(len(self.updated_list[1].get_list_of_graphs()), 0)

    def test_graphs_names(self):
        graph_listname = [ "gt1.kmer15.(1268000.1270000).V21.E27.cyc64", "gt1.kmer15.(1466000.1468000).V26.E35.cyc240", \
             "gt1.kmer15.(3194000.3196000).V22.E28.cyc64", "gt1.kmer15.(736000.738000).V22.E29.cyc128", "gt20.kmer15.(102000.104000).V75.E104.cyc1000"]
        graphs = self.updated_list[0].get_list_of_graphs()
        graph_names = [graph.get_names() for graph in graphs]
        graphs_alph = sorted(graph_names)
        for i in range(5):
            self.assertEqual(graphs_alph[i], graph_listname[i])
        self.assertListEqual(self.updated_list[1].get_list_of_graphs(), [])

    def test_statistics(self):
        self.assertEqual(self.updated_list[0].get_statistics(), (5, 33, 45, 166, 223))
        self.assertEqual(self.updated_list[1].get_statistics(), (0, 0, 0, 0, 0))

    def test_sources(self):
        self.assertEqual(len(self.updated_list[0].get_dataset_source()), 20)
        self.assertEqual(self.updated_list[0].get_dataset_source()[0], ('https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/005/845/GCA_000005845.2_ASM584v2/GCA_000005845.2_ASM584v2_genomic.fna.gz', 'GCA_000005845.2_ASM584v2.fna'))
        self.assertListEqual(self.updated_list[1].get_dataset_source(), [])

class TestReadGraphsNotVisible(unittest.TestCase):
    def setUp(self):
        self.dir = "./src/tests/testdata_for_dataset_reader"
        dataset1 = Dataset(True, True, True, self.dir+"/testdata_with_full_description", "name1", "desc1", "desc1", "MIT", False, "testdata_with_full_description")
        dataset2 = Dataset(True, True, True, self.dir+"/testdata_with_no_data", "name2", "desc2", "desc2", "GNU", False, "testdata_with_no_data")
        dataset_list = [dataset1, dataset2]
        self.readgraphs = ReadGraphs(dataset_list)
        self.readgraphs.run()
        self.updated_list = self.readgraphs.get_dataset_list_with_graphs()

    def test_returns_list(self):
        self.assertIsInstance(self.updated_list, list)

    def test_graphs_list_length_when_not_visible(self):
        self.assertEqual(len(self.updated_list), 0)
