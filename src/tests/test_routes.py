<<<<<<< HEAD
# import unittest
# from app import get_app
# from os import environ
=======
"""
import unittest
from app import get_app
from os import environ
>>>>>>> e85e5e524e0771ce9b8b6a11c8dd4cdb4c7b8c23

# class TestRoutes(unittest.TestCase):

#     def setUp(self):
#         self.app = get_app().test_client()
        
#     def test_index(self):
#         with self.app as test_client:
#             res = test_client.get("/index")
#             assert res.status_code == 200
        
<<<<<<< HEAD
#     def test_wrong_url_fails(self):
#         with self.app as test_client:
#             res = test_client.get("/xx")
#             assert res.status_code != 200
=======
    def test_wrong_url_fails(self):
        with self.app as test_client:
            res = test_client.get("/xx")
            assert res.status_code != 200
"""
>>>>>>> e85e5e524e0771ce9b8b6a11c8dd4cdb4c7b8c23
