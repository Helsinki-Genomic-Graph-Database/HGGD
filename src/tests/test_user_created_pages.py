import unittest
import os
import json


from src.website_creator.user_defined_page_creator import UserDefinedPageCreator
from src.app import get_app

class TestPageCreator(unittest.TestCase):

    def write_about(self):
        with open(self.folder+"/about.json", "w") as file:
            file.write(self.about)

    def write_howto(self):
        with open(self.folder+"/howto.json", "w") as file:
            file.write(self.howto)

    def remove_file(self, path):
        if os.path.exists(path):
            os.remove(path)

    def setUp(self):
        self.folder = os.getenv("USER_DEFINED_TEMPLATE_FOLDER")
        self.about = json.dumps({"name": "About", "content": "about tests"})
        self.howto = json.dumps({"name": "How to", "content": "like this"})

    def tearDown(self):
        self.remove_file(self.folder+"/about.json")
        self.remove_file(self.folder+"/howto.json")
        self.remove_file(self.folder+"/pages/about.html")
        self.remove_file(self.folder+"/pages/howto.html")

    def test_page_creator_should_make_a_dictionary_of_pages_from_json_files_in_templatefolder(self):

        self.write_about()

        self.write_howto()

        pcreator = UserDefinedPageCreator(self.folder)

        res = pcreator.get_pages()

        self.assertEqual(len(res), 2)

    def test_page_creator_list_should_give_dictionary_with_html_filename_as_key(self):
        self.write_about()
        pcreator = UserDefinedPageCreator(self.folder)
        res = pcreator.get_pages()
        print(res)
        self.assertEqual(res["about"], "About")
        

    def test_page_creator_should_create_html_file(self):
        self.write_about()
        pcreator = UserDefinedPageCreator(self.folder)
        res = os.path.exists(self.folder+"/pages/about.html")
        self.assertEqual(res, True)

    def test_created_page_should_exist_on_webpage(self):
        app = get_app().test_client()
        self.write_about()
        pcreator = UserDefinedPageCreator(self.folder)
        res = app.get("hggd/pages/about")
        self.assertEqual(res.status_code, 200)

    def test_created_page_has_content_text(self):
        app = get_app().test_client()
        self.write_about()
        pcreator = UserDefinedPageCreator(self.folder)
        res = app.get("hggd/pages/about").data
        self.assertIn(b"about tests", res)


