import unittest
from src.helper_functions_for_app import create_link_fo_fna

class TestLinkCreation(unittest.TestCase):

    def test_should_get_correct_link(self):
        res = create_link_fo_fna("GCA_000008865.2_ASM886v2.fna")
        self.assertEqual(res, "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/008/865/GCA_000008865.2_ASM886v2/GCA_000008865.2_ASM886v2_genomic.fna.gz")