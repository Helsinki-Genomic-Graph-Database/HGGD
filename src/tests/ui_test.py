import unittest
import os
import json
from io import StringIO
from time import sleep
from src.dataset_services.dataset_reader import DatasetReader
from src.dataset_services.dataset_creator import DatasetCreator
from src.data_check.ui import UI
from src.tests.stub_io import StubIO

class TestUI(unittest.TestCase):
    def setUp(self):
        self.reader = DatasetReader("src/tests/")
        self.dir_paths = self.reader.get_paths()
        self.creator = DatasetCreator(self.dir_paths)
        self.dataset_list = self.creator.get_datasets()
        self.dataset_dict = {}
        for dataset in self.dataset_list:
            name = dataset.get_folder_name()
            self.dataset_dict.update({name : dataset})

    def test_ask_name_(self):
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(self.dataset_list, io)
        response = ui.ask_name()

        self.assertEqual(response, "test_name")

    def test_ask_sh_desc(self):
        inputs = ["test_sh"]
        io = StubIO(inputs)
        ui = UI(self.dataset_list, io)
        response = ui.ask_sh_desc()

        self.assertEqual(response, "test_sh")

    def test_ask_long_desc(self):
        inputs = ["test_long"]
        io = StubIO(inputs)
        ui = UI(self.dataset_list, io)
        response = ui.ask_long_desc()

        self.assertEqual(response, "test_long")

    def test_ask_licence(self):
        inputs = ["test_licence"]
        io = StubIO(inputs)
        ui = UI(self.dataset_list, io)
        response = ui.ask_for_licence()

        self.assertEqual(response, "test_licence")

    def test_process_name_when_doesnt_exist(self):
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(self.dataset_list, io)
        dataset = self.dataset_dict["testdata_with_description_missing_name"]
        with open("src/tests/testdata_with_description_missing_name/description.json", "r+") as file:
            original = json.load(file)
        ui.process_name(dataset)
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
        strings_name = "\033[1;32;40mName exists.\033[0;37;40m"
        self.assertEqual(io.outputs[1], strings_name)

    def test_process_name_it_exists(self):
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(self.dataset_list, io)
        dataset = self.dataset_dict["testdata_with_full_description"]
        ui.process_name(dataset)
        strings_name = "\033[1;32;40mName exists.\033[0;37;40m"
        self.assertEqual(io.outputs[0], strings_name)

    def test_process_short_desc(self):
        inputs = ["test short desc"]
        io = StubIO(inputs)
        ui = UI(self.dataset_list, io)
        dataset = self.dataset_dict["test_json_for_processing_methods_short_desc"]
        with open("src/tests/test_json_for_processing_methods_short_desc/description.json", "r+") as file:
            original = json.load(file)
        ui.process_short_desc(dataset)
        with open("src/tests/test_json_for_processing_methods_short_desc/description.json", "r+") as file:
            content = json.load(file)
        with open("src/tests/test_json_for_processing_methods_short_desc/description.json", "w+") as file:
            json.dump(original, file)
        short_desc_exists = False
        if "descr_short" in content:
            short_desc_exists = True
        self.assertEqual(short_desc_exists, True)
        short_desc_in_content = content["descr_short"]
        self.assertEqual(short_desc_in_content, "test short desc")
        strings_short = "\033[1;32;40mShort description exists.\033[0;37;40m"
        self.assertEqual(io.outputs[1], strings_short)

    def test_process_long_desc_entering_long_desc(self):
        inputs = ["test long desc"]
        io = StubIO(inputs)
        ui = UI(self.dataset_list, io)
        dataset = self.dataset_dict["test_json_for_processing_methods_long_desc"]
        with open("src/tests/test_json_for_processing_methods_long_desc/description.json", "r+") as file:
            original = json.load(file)
        ui.process_long_description(dataset, False)
        with open("src/tests/test_json_for_processing_methods_long_desc/description.json", "r+") as file:
            content = json.load(file)
        long_desc_exists = False
        if "descr_long" in content:
            long_desc_exists = True
        with open("src/tests/test_json_for_processing_methods_long_desc/description.json", "w+") as file:
            json.dump(original, file)
        self.assertEqual(long_desc_exists, True)
        long_desc_in_content = content["descr_long"]
        self.assertEqual(long_desc_in_content, "test long desc")
        strings_long = "\033[1;32;40mLong description exists.\033[0;37;40m"
        self.assertEqual(io.outputs[1], strings_long)

    def test_process_long_desc_entering_no_long_desc(self):
        inputs = [""]
        io = StubIO(inputs)
        ui = UI(self.dataset_list, io)
        dataset = self.dataset_dict["test_json_for_processing_methods_long_desc"]
        with open("src/tests/test_json_for_processing_methods_long_desc/description.json", "r+") as file:
            original = json.load(file)
        ui.process_long_description(dataset, False)
        with open("src/tests/test_json_for_processing_methods_long_desc/description.json", "r+") as file:
            content = json.load(file)
        long_desc_exists = False
        if "descr_long" in content:
            long_desc_exists = True
        with open("src/tests/test_json_for_processing_methods_long_desc/description.json", "w+") as file:
            json.dump(original, file)
        self.assertEqual(long_desc_exists , True)
        long_desc_in_content = content["descr_long"]
        self.assertEqual(long_desc_in_content, "")
        strings_long = "\033[1;33;40mYou chose that the dataset \
doesn't have a long description.\033[0;37;40m"
        self.assertEqual(io.outputs[1], strings_long)

    def test_process_licence_enter_licence(self):
        inputs = ["test licence"]
        io = StubIO(inputs)
        ui = UI(self.dataset_list, io)
        dataset = self.dataset_dict["test_json_for_processing_methods_licence"]
        with open("src/tests/test_json_for_processing_methods_licence/description.json", "r+") as file:
            original = json.load(file)
        ui.process_licence(dataset, False)
        with open("src/tests/test_json_for_processing_methods_licence/description.json", "r+") as file:
            content = json.load(file)
        licence_exists = False
        if "licence" in content:
            licence_exists = True
        with open("src/tests/test_json_for_processing_methods_licence/description.json", "w+") as file:
            json.dump(original, file)
        self.assertEqual(licence_exists , True)
        licence_in_content = content["licence"]
        self.assertEqual(licence_in_content, "test licence")
        strings_licence = "\033[1;32;40mLicence exists.\033[0;37;40m"
        self.assertEqual(io.outputs[1], strings_licence)

    def test_process_licence_entering_no_licence(self):
        inputs = [""]
        io = StubIO(inputs)
        ui = UI(self.dataset_list, io)
        dataset = self.dataset_dict["test_json_for_processing_methods_licence"]
        with open("src/tests/test_json_for_processing_methods_licence/description.json", "r+") as file:
            original = json.load(file)
        ui.process_licence(dataset, False)
        with open("src/tests/test_json_for_processing_methods_licence/description.json", "r+") as file:
            content = json.load(file)
        licence_exists = False
        if "licence" in content:
            licence_exists = True
        with open("src/tests/test_json_for_processing_methods_licence/description.json", "w+") as file:
            json.dump(original, file)
        self.assertEqual(licence_exists, False)
        strings_licence = "\033[1;33;40mYou chose that the dataset \
doesn't have a licence.\033[0;37;40m"
        self.assertEqual(io.outputs[1], strings_licence)

    def test_start_all_data_correct(self):
        reader = DatasetReader("src/tests/ui_test_full_data")
        dir_paths = reader.get_paths()
        creator = DatasetCreator(dir_paths)
        dataset_list = creator.get_datasets()
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(dataset_list, io)
        ui.start()
        strings_path = "testdata_with_full_description"
        strings_data = "\033[1;32;40mData exists.\033[0;37;40m"
        strings_json = "\033[1;32;40mJson-file exists.\033[0;37;40m"
        strings_name = "\033[1;32;40mName exists.\033[0;37;40m"
        strings_short = "\033[1;32;40mShort description exists.\033[0;37;40m"
        strings_long = "\033[1;32;40mLong description exists.\033[0;37;40m"
        strings_licence = "\033[1;32;40mLicence exists.\033[0;37;40m"
        strings_graphs = "\033[1;32;40mAll graphs in dataset have a description.\033[0;37;40m"
        strings_checked = "Data has been checked."
        os.remove("src/tests/ui_test_full_data/testdata_with_full_description/log.txt")
        self.assertEqual(io.outputs[2], strings_path)
        self.assertEqual(io.outputs[5], strings_data)
        self.assertEqual(io.outputs[6], strings_json)
        self.assertEqual(io.outputs[7], strings_name)
        self.assertEqual(io.outputs[8], strings_short)
        self.assertEqual(io.outputs[9], strings_long)
        self.assertEqual(io.outputs[10], strings_licence)
        self.assertEqual(io.outputs[11], strings_graphs)
        self.assertEqual(io.outputs[12], strings_checked)

    def test_start_no_data(self):
        reader = DatasetReader("src/tests/ui_test_no_data")
        dir_paths = reader.get_paths()
        creator = DatasetCreator(dir_paths)
        dataset_list = creator.get_datasets()
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(dataset_list, io)
        ui.start()
        strings_data = "\x1b[1;33;40mThere is no data in folder testdata_with_no_data.\x1b[0;37;40m"
        self.assertEqual(io.outputs[5], strings_data)

    def test_start_empty_description_enter_all_fields(self):
        reader = DatasetReader("src/tests/ui_test_empty_desc/")
        dir_paths = reader.get_paths()
        creator = DatasetCreator(dir_paths)
        dataset_list = creator.get_datasets()
        inputs = ["test_name", "test_short_desc", "long_desc", "MIT"]
        io = StubIO(inputs)
        ui = UI(dataset_list, io)
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
        strings_graphs = "\033[1;32;40mAll graphs in dataset have a description.\033[0;37;40m"
        strings_checked = "Data has been checked and updated."
        open("src/tests/ui_test_empty_desc/testdata_with_empty_description/description.json", 'w').close()
        os.remove("src/tests/ui_test_empty_desc/testdata_with_empty_description/log.txt")
        self.assertEqual(io.outputs[6], strings_name)
        self.assertEqual(io.outputs[7], strings_short)
        self.assertEqual(io.outputs[8], strings_long)
        self.assertEqual(io.outputs[9], strings_licence)
        self.assertEqual(io.outputs[10], strings_json)
        self.assertEqual(io.outputs[11], strings_name2)
        self.assertEqual(io.outputs[12], strings_short2)
        self.assertEqual(io.outputs[13], strings_long2)
        self.assertEqual(io.outputs[14], strings_licence2)
        self.assertEqual(io.outputs[15], strings_graphs)
        self.assertEqual(io.outputs[16], strings_checked)

    def test_start_empty_description_enter_no_long_desc_or_licence(self):
        reader = DatasetReader("src/tests/ui_test_empty_desc/")
        dir_paths = reader.get_paths()
        creator = DatasetCreator(dir_paths)
        dataset_list = creator.get_datasets()
        inputs = ["test_name", "test_short_desc", "", ""]
        io = StubIO(inputs)
        ui = UI(dataset_list, io)
        ui.start()
        strings_long = "\033[1;33;40mYou chose that the dataset \
doesn't have a long description.\033[0;37;40m"
        strings_licence = "\033[1;33;40mYou chose that the dataset doesn't have a licence.\033[0;37;40m"
        open("src/tests/ui_test_empty_desc/testdata_with_empty_description/description.json", 'w').close()
        os.remove("src/tests/ui_test_empty_desc/testdata_with_empty_description/log.txt")
        self.assertEqual(io.outputs[13], strings_long)
        self.assertEqual(io.outputs[14], strings_licence)


    def test_start_new_file_but_all_data_correct(self):
        with open("src/tests/ui_test_full_data/testdata_with_full_description/log.txt", 'w') as log:
            log.write("test")
        sleep(0.05)
        with open("src/tests/ui_test_full_data/testdata_with_full_description/test.txt", 'w') as test:
            test.write("test")
        reader = DatasetReader("src/tests/ui_test_full_data")
        dir_paths = reader.get_paths()
        creator = DatasetCreator(dir_paths)
        dataset_list = creator.get_datasets()
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(dataset_list, io)
        ui.start()
        strings_path = "testdata_with_full_description"
        strings_data = "\033[1;32;40mData exists.\033[0;37;40m"
        strings_json = "\033[1;32;40mJson-file exists.\033[0;37;40m"
        strings_name = "\033[1;32;40mName exists.\033[0;37;40m"
        strings_short = "\033[1;32;40mShort description exists.\033[0;37;40m"
        strings_long = "\033[1;32;40mLong description exists.\033[0;37;40m"
        strings_licence = "\033[1;32;40mLicence exists.\033[0;37;40m"
        strings_graphs = "\033[1;32;40mAll graphs in dataset have a description.\033[0;37;40m"
        strings_checked = "Data has been checked and updated."
        os.remove("src/tests/ui_test_full_data/testdata_with_full_description/log.txt")
        os.remove("src/tests/ui_test_full_data/testdata_with_full_description/test.txt")
        self.assertEqual(io.outputs[2], strings_path)
        self.assertEqual(io.outputs[5], strings_data)
        self.assertEqual(io.outputs[6], strings_json)
        self.assertEqual(io.outputs[7], strings_name)
        self.assertEqual(io.outputs[8], strings_short)
        self.assertEqual(io.outputs[9], strings_long)
        self.assertEqual(io.outputs[10], strings_licence)
        self.assertEqual(io.outputs[11], strings_graphs)
        self.assertEqual(io.outputs[12], strings_checked)

    def test_start_log_file_newest(self):
        with open("src/tests/ui_test_full_data/testdata_with_full_description/log.txt", 'w') as log:
            log.write("test")
        sleep(0.05)
        reader = DatasetReader("src/tests/ui_test_full_data")
        dir_paths = reader.get_paths()
        creator = DatasetCreator(dir_paths)
        dataset_list = creator.get_datasets()
        inputs = ["test_name"]
        io = StubIO(inputs)
        ui = UI(dataset_list, io)
        ui.start()
        string_done = "Folder done."
        os.remove("src/tests/ui_test_full_data/testdata_with_full_description/log.txt")
        self.assertEqual(io.outputs[5], string_done)
