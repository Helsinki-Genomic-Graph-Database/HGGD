import unittest
import json
from src.data_check.json_writer import JsonWriter
from src.entities.dataset import Dataset

class TestJsonWriter(unittest.TestCase):

    def setUp(self):
        self.writer = JsonWriter()
        self.dataset_one = Dataset(description_file_exists = True, data_exists = True, licence_file_exists = False, path = "src/tests/ui_test_empty_desc/testdata_with_empty_description", name = "", descr_short = "", descr_long = "", licence ="", show_on_website = False, folder_name = "", user_defined_columns = None)
        self.dataset_two = Dataset(description_file_exists = True, data_exists = True, licence_file_exists = False, path = "src/tests/testdata_with_description_missing_name/", name = "", descr_short = "", descr_long = "", licence ="", show_on_website = False, folder_name = "", user_defined_columns = None)

    def test_create_json_file(self):
        self.writer.create_json_file(self.dataset_one, "test_name", "test_short_desc", "long_desc", "MIT")
        with open("src/tests/ui_test_empty_desc/testdata_with_empty_description/description.json", "r+") as file:
            content = json.load(file)
            content = str(content)
        open("src/tests/ui_test_empty_desc/testdata_with_empty_description/description.json", 'w').close()
        self.assertEqual(content, "{'name': 'test_name', 'descr_short': 'test_short_desc', 'descr_long': 'long_desc', 'licence': 'MIT'}")

    def test_update_json_file(self):
        with open("src/tests/testdata_with_description_missing_name/description.json", "r+") as file:
            original = json.load(file)
        self.writer.update_json_file(self.dataset_two, "name", "test_name")
        with open("src/tests/testdata_with_description_missing_name/description.json", "r+") as file:
            content = json.load(file)
        with open("src/tests/testdata_with_description_missing_name/description.json", "w+") as file:
            json.dump(original, file)
        name_exists = False
        if "name" in content:
            name_exists = True
        self.assertEqual(name_exists, True)
        name_in_content = content["name"]
        self.assertEqual(name_in_content, "test_name")
