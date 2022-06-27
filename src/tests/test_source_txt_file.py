import unittest
import os
import shutil
from src.dataset_services.dataset_creator import DatasetCreator
from src.website_creator.read_graphs import ReadGraphs
from src.entities.dataset import Dataset

class TestSourceTxtFileForDataset(unittest.TestCase):
    def setUp(self):
        self.directory = "src/tests/testdata_for_dataset_reader/testdata_with_full_description"
        
        self.dataset = Dataset(True, True, True, self.directory, "name1", "desc1", "desc1", "MIT", True, "testdata_with_full_description")


    def test_dataset_source_txt_file_correct(self):
        self.delete_source_txt_folder()
        graph_update_service = ReadGraphs([self.dataset])
        graph_update_service.run()
        with open("src/tests/testdata_for_dataset_reader/testdata_with_full_description/sourcetxt/testdata_with_full_description.txt", "r") as file:
            contents = file.readlines()
        self.assertEqual(len(contents), 20)
        self.assertEqual(contents[0].rstrip("\n"), "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/005/845/GCA_000005845.2_ASM584v2/GCA_000005845.2_ASM584v2_genomic.fna.gz")
        self.assertEqual(contents[19].rstrip("\n"), "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/021/125/GCA_000021125.1_ASM2112v1/GCA_000021125.1_ASM2112v1_genomic.fna.gz")
  
    def test_graph_source_txt_file_correct(self):
        self.delete_source_txt_folder()
        graph_update_service = ReadGraphs([self.dataset])
        graph_update_service.run()    
        with open("src/tests/testdata_for_dataset_reader/testdata_with_full_description/sourcetxt/graphs/gt1.kmer15.(736000.738000).V22.E29.cyc128.txt", "r") as file:
            contents = file.readlines()
        self.assertEqual(len(contents), 1)
        self.assertEqual(contents[0].rstrip("\n"), "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/005/845/GCA_000005845.2_ASM584v2/GCA_000005845.2_ASM584v2_genomic.fna.gz")


    def delete_source_txt_folder(self):
        print(os.listdir(self.directory))
        if os.path.exists(self.directory+"/sourcetxt"):
            print(self.directory+"/sourcetxt")
            shutil.rmtree(self.directory+"/sourcetxt")        


