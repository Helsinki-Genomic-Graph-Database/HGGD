import json
import os
import json
from src.file_ui.file_utils import check_file_extension

class FolderReader:
    """
    get_folder_info() runs the scan and returns the list
    """

    def __init__(self, paths):
        self.paths = paths
        self.info_list = []

    def get_folder_info(self):
        self.run()
        return self.info_list

    def run(self):
        for path in self.paths:
            self.read_folder(path)

    def read_folder(self, path):

        data_exists = False
        _description_found = False
        description_file_exists = False
        name_exists = False
        descr_short_exists = False
        descr_long_exists = False

        files = os.listdir(path)

        for filename in files:

            if check_file_extension(filename, "graph"):
                data_exists = True

            if filename == "description.json":
                if _description_found:
                    description_file_exists = False
                else:
                    description_file_exists = True
                    _description_found = True
                    name_exists, descr_short_exists, descr_long_exists = self.read_json(path,filename)

        self.info_list.append((path,data_exists,description_file_exists,name_exists, descr_short_exists, descr_long_exists))

    def read_json(self, path, filename):
        name = False
        descr_short = False
        descr_long = False
        filepath = f"{path}/{filename}"
        if os.stat(filepath).st_size > 0:
            file = open(filepath)
            content = json.load(file)
            if len(content["name"]) > 0:
                name = True
            if len(content["descr_short"]) > 0:
                descr_short = True
            if len(content["descr_long"]) > 0:
                descr_long = True

        return (name,descr_short,descr_long)