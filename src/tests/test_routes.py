"""
import unittest
from src.app import get_app

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = get_app().test_client()

    def test_index(self):
        with self.app as test_client:
            res = test_client.get("/index")
            assert res.status_code == 200
        
    def test_wrong_url_fails(self):
        with self.app as test_client:
            res = test_client.get("/xx")
            assert res.status_code != 200

"""