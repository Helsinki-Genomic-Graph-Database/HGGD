import unittest
from src.file_ui.file_utils import read_description

class TestDescriptionReader(unittest.TestCase):

    def test_reader(self):
        name, descr_short, descr_long, licence, user_defined_columns, sources = read_description("src/tests/testdata_with_full_description")
        self.assertEqual(name, "testdata with description")
        self.assertEqual(descr_long, "testing data")
        self.assertEqual(descr_short, "with full description")
        self.assertEqual(licence, "MIT")
        self.assertEqual(sources, [("test source", "test source"), ("test source2", "test source2")])
