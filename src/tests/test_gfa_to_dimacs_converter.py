import os
import shutil
import unittest
from time import sleep
from src.data_check.gfa_to_dimacs_converter import GfaToDimacsConverter

class TestGraphToDimacsConverter(unittest.TestCase):
    def setUp(self):
        self.directory = "src/tests/testdata_for_gfa_to_dimacs_converter"
        self.converter = GfaToDimacsConverter(self.directory)
        self.filename_gfa = "sample.gfa"
        self.filename_dimacs = "sample.dimacs"

    def tearDown(self):
        self.delete_dimacs_folder()

    def test_converted_file_correct(self):
        self.converter.convert_gfa_to_dimacs(self.filename_gfa)
        with open(os.path.join(f"{self.directory}/dimacs", self.filename_dimacs), "r") as file:
            information = file.read().split("\n")
            self.assertEqual("p edge 10 10", str(information[0]))
            self.assertEqual("e 1 3", str(information[1]))
            self.assertEqual("e 4 2", str(information[2]))
            self.assertEqual("e 3 1", str(information[3]))
            self.assertEqual("e 2 4", str(information[4]))
            self.assertEqual("e 5 3", str(information[5]))
            self.assertEqual("e 4 6", str(information[6]))
            self.assertEqual("e 5 7", str(information[7]))
            self.assertEqual("e 8 6", str(information[8]))
            self.assertEqual("e 7 9", str(information[9]))
            self.assertEqual("e 10 8", str(information[10]))

    def test_convert_no_dimacs_folder(self):
        self.delete_dimacs_folder()
        self.converter.convert_gfa_to_dimacs(self.filename_gfa)
        res = os.path.exists(f"{self.directory}/dimacs/{self.filename_dimacs}")
        self.assertEqual(res, True)

    def test_convert_dimacs_folder_exists_no_dimacs_file(self):
        self.make_dimacs_folder()
        sleep(0.05)
        c_time = os.path.getctime(f"{self.directory}/dimacs") # creation time
        self.converter.convert_gfa_to_dimacs(self.filename_gfa)
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
        self.converter.convert_gfa_to_dimacs(self.filename_gfa)
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
