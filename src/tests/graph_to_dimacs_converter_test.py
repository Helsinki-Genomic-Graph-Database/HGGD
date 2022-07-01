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

    def test_converted_file_correct(self):
        self.converter.convert_graph_to_dimacs(self.filename_graph)
        with open(os.path.join(f"{self.directory}/dimacs", self.filename_dimacs), "r") as file:
            information = file.read().split("\n")
            self.assertEqual("c unique source is 0, unique sink is 1", str(information[0]))
            self.assertEqual("c genomes: GCA_000005845.2_ASM584v2.fna ", str(information[1]))
            self.assertEqual("c ground truth paths, in the format 'weight node1 node2 node3 ... '", str(information[2]))
            self.assertEqual("c 16 0 303 328 334 384 469 514 550 558 573 602 617 650 665 669 303 328 334 690 384 469 775 514 810 550 558 824 573 602 838 617 650 852 665 669 328 334 690 1 ", str(information[3]))
            self.assertEqual("c List of edges with weights: e 303 328 32, e 303 328 32, e 328 334 48, e 334 384 16, e 334 690 32, e 384 469 32, e 469 514 16, e 469 775 16, e 514 550 16, e 514 810 16, e 550 558 32, e 558 573 16, e 558 824 16, e 573 602 32, e 602 617 16, e 602 838 16, e 617 650 32, e 650 665 16, e 650 852 16, e 665 669 32, e 669 303 16, e 669 328 16, e 690 1 16, e 690 384 16, e 775 514 16, e 810 550 16, e 824 573 16, e 838 617 16, e 852 665 16, e 0 303 16", str(information[4]))
            self.assertEqual("p edge 22 30", str(information[5]))
            self.assertEqual("e  303 328", str(information[6]))
            self.assertEqual("e  328 334", str(information[7]))

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