
import unittest
from src.website_creator.graph_reader import GraphReader

class TestGraphReaderWithFullDescription(unittest.TestCase):

    def setUp(self):
        DIR = "src/tests/testdata_for_graph_with_graph_desc/full_desc"
        self.graphcreator = GraphReader(DIR)

    # def test_read_file_full_desc(self):
    #     name, nodes, edges, sources, licence, comments_for_conversion, edges_listed, short_desc = self.graphcreator.read_file("gt1.kmer15.(736000.738000).V22.E29.cyc128.graph")
    #     self.assertEqual(name, "test graph")
    #     self.assertEqual(nodes, 22)
    #     self.assertEqual(edges, 29)
    #     self.assertEqual(licence, "MIT")
    #     self.assertEqual(sources, [("test source1", "test source1")]) 
    #     self.assertEqual(short_desc, "short")

    def test_read_file_no_desc(self):
        name, nodes, edges, sources, licence, comments_for_conversion, edges_listed, short_desc = self.graphcreator.read_file("gt1.kmer15.(1268000.1270000).V21.E27.cyc64.graph")
        self.assertEqual(name, "gt1.kmer15.(1268000.1270000).V21.E27.cyc64")
        self.assertEqual(nodes, 21)
        self.assertEqual(edges, 27)
        self.assertEqual(licence, None)
        self.assertEqual(sources, [('https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/005/845/GCA_000005845.2_ASM584v2/GCA_000005845.2_ASM584v2_genomic.fna.gz', 'GCA_000005845.2_ASM584v2.fna')])
        self.assertEqual(licence, None)
        self.assertEqual(short_desc, None)

# class TestGraphReaderWithInadequateDescription(unittest.TestCase):

#     def setUp(self):
#         DIR = "src/tests/testdata_for_graph_with_graph_desc/inadequate_desc"
#         self.graphcreator = GraphReader(DIR)

#     def test_read_file_full_desc(self):
#         name, nodes, edges, sources, licence, comments_for_conversion, edges_listed, short_desc = self.graphcreator.read_file("gt1.kmer15.(736000.738000).V22.E29.cyc128.graph")
#         self.assertEqual(name, "gt1.kmer15.(736000.738000).V22.E29.cyc128")
#         self.assertEqual(nodes, 22)
#         self.assertEqual(edges, 29)
#         self.assertEqual(licence, None)
#         self.assertEqual(sources, [("graph source1", "graph source1"), ("graph source2", "graph source2")]) 
#         self.assertEqual(short_desc, "sh")