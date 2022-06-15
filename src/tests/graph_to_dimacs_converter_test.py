import os
import shutil
import unittest
from time import sleep
from src.data_check.graph_to_dimacs_converter import GraphToDimacsConverter

class TestGraphToDimacsConverter(unittest.TestCase):
    def setUp(self):
        self.directory = "src/tests/testdata_for_graph_to_dimacs_converter"
        self.converter = GraphToDimacsConverter(self.directory)
        self.filename_graph = "gt1.kmer15.(736000.738000).V22.E29.cyc128.graph"
        self.filename_dimacs = "gt1.kmer15.(736000.738000).V22.E29.cyc128.dimacs"

    def tearDown(self):
        self.delete_dimacs_folder()

    def test_convert_no_dimacs_folder(self):
        self.delete_dimacs_folder()
        self.converter.convert_graph_to_dimacs(self.filename_graph)
        res = os.path.exists(f"{self.directory}/dimacs/{self.filename_dimacs}")
        self.assertEqual(res, True)

    def test_convert_dimacs_folder_exists_no_dimacs_file(self):
        self.make_dimacs_folder()
        sleep(0.05)
        c_time = os.path.getctime(f"{self.directory}/dimacs") # creation time
        self.converter.convert_graph_to_dimacs(self.filename_graph)
        m_time = os.path.getmtime(f"{self.directory}/dimacs") # modification time
        res1 = os.path.exists(f"{self.directory}/dimacs/{self.filename_dimacs}")
        self.assertEqual(res1, True) # file exists
        res2 = c_time == m_time
        self.assertEqual(res2, False) # folder was updated

    def test_convert_dimacs_folder_and_file_exist(self):
        self.make_dimacs_folder()
        self.make_dimacs_file(f"{self.directory}/dimacs")
        sleep(0.05)
        c_time = os.path.getctime(f"{self.directory}/dimacs/{self.filename_dimacs}") # creation time
        self.converter.convert_graph_to_dimacs(self.filename_graph)
        m_time = os.path.getmtime(f"{self.directory}/dimacs/{self.filename_dimacs}") # modification time
        res2 = c_time == m_time
        self.assertEqual(res2, False) # file was updated

    def delete_dimacs_folder(self):
        if os.path.exists(f"{self.directory}/dimacs"):
            shutil.rmtree(f"{self.directory}/dimacs")

    def make_dimacs_folder(self):
        os.mkdir(f"{self.directory}/dimacs")

    def make_dimacs_file(self, directory):
        open(os.path.join(directory, self.filename_dimacs), 'w').close()