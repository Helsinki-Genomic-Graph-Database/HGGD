import unittest
import os
import shutil
from src.dataset_services.dataset_creator import DatasetCreator
from src.dataset_services.dataset_reader import DatasetReader
from src.tests.mock_spdx import SpdxService

class TestSourceTxtFileForDataset(unittest.TestCase):
    def setUp(self):
        self.data_directory = "src/tests/testdata_for_dataset_reader/testdata_with_full_description"
        self.spdx_service = SpdxService()
        self.reader = DatasetReader(self.data_directory)
        self.dir_paths = self.reader.get_paths()
        self.creator = DatasetCreator([self.data_directory], self.spdx_service)

    def test_dataset_source_txt_file_correct(self):
        self.delete_source_txt_folder()
        self.dataset = self.creator.get_datasets()[0]
        with open("src/tests/testdata_for_dataset_reader/testdata_with_full_description/sourcetxt/testdata_with_full_description.txt", "r") as file:
            contents = file.readlines()
        contents[-1] = contents[-1]+('\n')
        self.assertEqual(len(contents), 20)
        self.assertIn("https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/013/305/GCA_000013305.1_ASM1330v1/GCA_000013305.1_ASM1330v1_genomic.fna.gz\n", contents)
        self.assertIn("https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/019/385/GCA_000019385.1_ASM1938v1/GCA_000019385.1_ASM1938v1_genomic.fna.gz\n", contents)
  
    def test_graph_source_txt_file_correct(self):
        self.delete_source_txt_folder() 
        self.dataset = self.creator.get_datasets()[0]
        with open("src/tests/testdata_for_dataset_reader/testdata_with_full_description/sourcetxt/graphs/gt1.kmer15.(736000.738000).V22.E29.cyc128.txt", "r") as file:
            contents = file.readlines()
        self.assertEqual(len(contents), 1)
        self.assertEqual(contents[0].rstrip("\n"), "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/005/845/GCA_000005845.2_ASM584v2/GCA_000005845.2_ASM584v2_genomic.fna.gz")


    def delete_source_txt_folder(self):
        if os.path.exists(self.data_directory+"/sourcetxt"):
            shutil.rmtree(self.data_directory+"/sourcetxt")        


