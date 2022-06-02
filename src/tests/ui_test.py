import unittest
import os
import json
from io import StringIO
from src.file_ui.folder_reader import FolderReader
from src.text_ui.ui import UI
from src.tests.stub_io import StubIO

class TestUI(unittest.TestCase):
    def setUp(self):
        self.fr = FolderReader(["src/tests/testdata_with_full_description"])

    def test_ask_name_(self):
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(self.fr, io)
        response = ui.ask_name()

        self.assertEqual(response, "test_name")

    def test_ask_sh_desc(self):
        inputs = ["test_sh"]
        io = StubIO(inputs)
        ui = UI(self.fr, io)
        response = ui.ask_sh_desc()

        self.assertEqual(response, "test_sh")

    def test_ask_long_desc(self):
        inputs = ["test_long"]
        io = StubIO(inputs)
        ui = UI(self.fr, io)
        response = ui.ask_long_desc()

        self.assertEqual(response, "test_long")

    def test_start_all_data_correct(self):
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(self.fr, io)
        ui.start()
        strings_path = "src/tests/testdata_with_full_description"
        strings_data = "\033[1;32;40mData exists.\033[0;37;40m"
        strings_json = "\033[1;32;40mJson-file exists.\033[0;37;40m"
        strings_name = "\033[1;32;40mName exists.\033[0;37;40m"
        strings_short = "\033[1;32;40mShort description exists.\033[0;37;40m"
        strings_long = "\033[1;32;40mLong description exists.\033[0;37;40m"
        strings_licence = "\033[1;32;40mLicence exists.\033[0;37;40m"
        self.assertEqual(io.outputs[2], strings_path)
        self.assertEqual(io.outputs[3], strings_data)
        self.assertEqual(io.outputs[4], strings_json)
        self.assertEqual(io.outputs[5], strings_name)
        self.assertEqual(io.outputs[6], strings_short)
        self.assertEqual(io.outputs[7], strings_long)
        self.assertEqual(io.outputs[8], strings_licence)

    def test_start_no_data(self):
        fr = FolderReader(["src/tests/testdata_with_no_data"])
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(fr, io)
        ui.start()
        strings_data = "\x1b[1;33;40mThere is not data in folder src/tests/testdata_with_no_data.\x1b[0;37;40m"

        print(io.outputs)
        self.assertEqual(io.outputs[3], strings_data)

    def test_start_empty_description_enter_all_fields(self):
        fr = FolderReader(["src/tests/testdata_with_empty_description/"])
        inputs = ["test_name", "test_short_desc", "long_desc", "MIT"]
        io = StubIO(inputs)
        ui = UI(fr, io)
        ui.start()
        strings_json = "\033[1;32;40mJson-file exists.\033[0;37;40m"
        strings_name = "\033[1;31;40mThe dataset has no name.\033[0;37;40m"
        strings_short = "\033[1;31;40mThe dataset doesn't \
have a short description.\033[0;37;40m"
        strings_long = "\033[1;31;40mThe dataset doesn't have a long description.\033[0;37;40m"
        strings_licence = "\033[1;31;40mThe dataset has no licence.\033[0;37;40m"
        strings_name2 = "\033[1;32;40mName exists.\033[0;37;40m"
        strings_short2 = "\033[1;32;40mShort description exists.\033[0;37;40m"
        strings_long2 = "\033[1;32;40mLong description exists.\033[0;37;40m"
        strings_licence2 = "\033[1;32;40mLicence exists.\033[0;37;40m"
        open("src/tests/testdata_with_empty_description/description.json", 'w').close()
        self.assertEqual(io.outputs[4], strings_name)
        self.assertEqual(io.outputs[5], strings_short)
        self.assertEqual(io.outputs[6], strings_long)
        self.assertEqual(io.outputs[7], strings_licence)
        self.assertEqual(io.outputs[8], strings_json)
        self.assertEqual(io.outputs[9], strings_name2)
        self.assertEqual(io.outputs[10], strings_short2)
        self.assertEqual(io.outputs[11], strings_long2)
        self.assertEqual(io.outputs[12], strings_licence2)

    def test_start_empty_description_enter_no_long_desc_or_licence(self):
        fr = FolderReader(["src/tests/testdata_with_empty_description/"])
        inputs = ["test_name", "test_short_desc", "", ""]
        io = StubIO(inputs)
        ui = UI(fr, io)
        ui.start()
        strings_long = "\033[1;33;40mYou chose that the dataset doesn't have a long description.\033[1;37;40m"
        strings_licence = "\033[1;33;40mYou chose that the dataset doesn't have a licence.\033[0;37;40m"
        open("src/tests/testdata_with_empty_description/description.json", 'w').close()
        self.assertEqual(io.outputs[11], strings_long)
        self.assertEqual(io.outputs[12], strings_licence)

    def test_create_json_file(self):
        inputs = ["test_name", "test_short_desc", "long_desc", "MIT"]
        io = StubIO(inputs)
        ui = UI(self.fr, io)
        ui.start()
        ui.create_json_file("src/tests/testdata_with_empty_description/test_description.json","test_name", "test_short_desc", "long_desc", "MIT")
        with open("src/tests/testdata_with_empty_description/test_description.json", "r+") as file:
            content = json.load(file)
            content = str(content)
        os.remove("src/tests/testdata_with_empty_description/test_description.json")
        self.assertEqual(content, "{'name': 'test_name', 'descr_short': 'test_short_desc', 'descr_long': 'long_desc', 'licence': 'MIT'}")

    def test_update_json_file(self):
        inputs = ["test_name", "test_short_desc", "long_desc", "MIT"]
        io = StubIO(inputs)
        ui = UI(self.fr, io)
        ui.start()
        with open("src/tests/testdata_with_description_missing_name/description.json", "r+") as file:
            original = json.load(file)
            print(original)
        ui.update_json_file("src/tests/testdata_with_description_missing_name/description.json", "name", "test_name")
        with open("src/tests/testdata_with_description_missing_name/description.json", "r+") as file:
            content = json.load(file)
        with open("src/tests/testdata_with_description_missing_name/description.json", "w+") as file:
            json.dump(original, file)
        if "name" in content:
            name_exists = True
        name_in_content = content["name"]
        self.assertEqual(name_exists, True)
        self.assertEqual(name_in_content, "test_name")
