import unittest
from src.website_creator.gfa_reader import GfaReader

class TestGfaReader(unittest.TestCase):
    def setUp(self):
        DIR = "src/tests/testdata_for_gfa/gfa_example"
        
        self.gfareader_service = GfaReader(DIR)

    def test_read_file(self):
        name, nodes, edges, sources = self.gfareader_service.read_file("sample.gfa")
        self.assertEqual(name, "sample")
        self.assertEqual(nodes, 6)
        self.assertEqual(edges, 4)
        self.assertEqual(sources, [("https://www.testing.fi", "www.testing.fi")])
