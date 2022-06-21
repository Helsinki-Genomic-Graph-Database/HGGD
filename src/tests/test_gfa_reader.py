import unittest
from src.website_creator.gfa_reader import GfaReader

class TestGfaReader(unittest.TestCase):
    def setUp(self):
        DIR = "src/tests/testdata_for_gfa/gfa_example"       
        self.gfareader_service = GfaReader(DIR)

    def test_read_file(self):
        name, nodes, edges, sources, licence, short_desc = self.gfareader_service.read_file("sample.gfa")
        self.assertEqual(name, "sample")
        self.assertEqual(nodes, 6)
        self.assertEqual(edges, 4)
        self.assertEqual(sources, [])
        self.assertEqual(licence, None)
        self.assertEqual(short_desc, None)
        name, nodes, edges, sources, licence, short_desc = self.gfareader_service.read_file("sample2.gfa")
        self.assertEqual(name, "sample2")
        self.assertEqual(nodes, 4)
        self.assertEqual(edges, 3)
        self.assertEqual(sources, [])
        self.assertEqual(licence, None)
        self.assertEqual(short_desc, None)

# class TestGfaReaderWithDescription(unittest.TestCase):
#     def setUp(self):
#         DIR = "src/tests/testdata_for_gfa/gfa_example_with_description"     
#         self.gfareader_service = GfaReader(DIR)

#     def test_read_file(self):
#         name, nodes, edges, sources, licence, short_desc = self.gfareader_service.read_file("sample.gfa")
#         self.assertEqual(name, "testgfa")
#         self.assertEqual(nodes, 8)
#         self.assertEqual(edges, 4)
#         self.assertEqual(sources, [("gfa source1", "gfa source1"), ("gfa source2", "gfa source2")])
#         self.assertEqual(licence, "gfa licence")
#         self.assertEqual(short_desc, "short")
#         name, nodes, edges, sources, licence, short_desc  = self.gfareader_service.read_file("sample2.gfa")
#         self.assertEqual(name, "sample2")
#         self.assertEqual(nodes, 5)
#         self.assertEqual(edges, 3)
#         self.assertEqual(sources, [])
#         self.assertEqual(licence, None)
#         self.assertEqual(licence, None)

class TestGfaReaderWithNoNameDescription(unittest.TestCase):
    def setUp(self):
        DIR = "src/tests/testdata_for_gfa/gfa_example_with_no_name_desc"        
        self.gfareader_service = GfaReader(DIR)

    def test_read_file(self):
        name, nodes, edges, sources, licence, short_desc  = self.gfareader_service.read_file("sample.gfa")
        self.assertEqual(name, "sample")
        self.assertEqual(nodes, 7)
        self.assertEqual(edges, 2)
        self.assertEqual(sources, [])
        #self.assertEqual(licence, "gfa licence")
        self.assertEqual(short_desc, None)
