import unittest
from src.app import get_app

class TestRoutes(unittest.TestCase):
    #these test use the e_coli1-datafolder and assume the data there won't be altered
    def setUp(self):
        self.app = get_app().test_client()
        self.dataset = 'testdata_with_full_description'
        self.graph = 'gt1.kmer15.(736000.738000).V22.E29.cyc128'

    def test_index(self):
        with self.app as test_client:
            res = test_client.get("/hggd/index")
            assert res.status_code == 200
            assert b'<hy-heading heading="h1"> Helsinki Genomic Graph Database</hy-heading>' in res.data
            assert b'<hy-heading heading="h3"> Datasets in database </hy-heading>' in res.data
        
    def test_wrong_url_fails(self):
        with self.app as test_client:
            res = test_client.get("/xx")
            assert res.status_code != 200

    def test_datasetpage(self):
        with self.app as test_client:
            res = test_client.get(f"/hggd/datasets/{self.dataset}")
            assert res.status_code == 200
            assert b'<hy-paragraph-text>Total number of graphs in dataset:</hy-paragraph-text>' in res.data
            assert b'<hy-heading heading="h2"> testdata with description </hy-heading>' in res.data

    def test_graph_page(self):
        with self.app as test_client:
            res = test_client.get(f"/hggd/datasets/{self.dataset}/{self.graph}")
            assert res.status_code == 200
            assert b'<hy-heading heading="h5">Source files for the graph </hy-heading>' in res.data
            assert b'<hy-heading heading="h2"> gt1.kmer15.(736000.738000).V22.E29.cyc128</hy-heading>' in res.data

    def test_dataset_source_page(self):
        with self.app as test_client:
            res = test_client.get(f"/hggd/datasets/{self.dataset}/sources")
            assert res.status_code == 200
            assert b'<hy-heading heading="h5">Source files </hy-heading>' in res.data
            assert b'<hy-heading heading="h2"> Source links for testdata with description</hy-heading>' in res.data
