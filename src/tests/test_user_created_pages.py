import unittest
import os
import json

from src.website_creator.user_defined_page_creator import UserDefinedPageCreator

class TestPageCreator(unittest.TestCase):

    def setUp(self):
        self.folder = "src/tests/mock_templatefolder"
        self.about = json.dumps({"name": "about", "content": "about tests"})
        self.howto = json.dumps({"name": "how to", "content": "like this"})

    def test_page_creator_should_make_a_list_of_pages_from_json_files_in_templatefolder(self):

        with open(self.folder+"/about.json", "w") as file:
            file.write(self.about)

        with open(self.folder+"/howto.json", "w") as file:
            file.write(self.howto)

        pcreator = UserDefinedPageCreator(self.folder)

        res = pcreator.get_pages()

        self.assertEqual(len(res), 2)

    # def test_page_creator_list_should_have