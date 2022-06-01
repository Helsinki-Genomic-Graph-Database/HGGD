import json
import os
from src.file_ui.file_utils import check_file_extension

class FolderReader:
    """
    get_folder_info() runs the scan of folders given and returns the list of info of the folders,
    format: [(path of folder:str, graph files exist:bool, description file exists:bool,
    description file has name:bool, description file exists:bool,
    description file has short description:bool,
    description file exists:bool, description file has long description:bool)]
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
        description_file_exists = False
        name_exists = False
        descr_short_exists = False
        descr_long_exists = False
        licence_exists = False
        ui_run = False

        files = os.listdir(path)

        for filename in files:

            if check_file_extension(filename, "graph"):
                data_exists = True

            if filename == "description.json":
                description_file_exists = True
                name_exists, descr_short_exists, descr_long_exists, \
                licence_exists = self.read_json(path,filename)

        self.info_list.append((path,data_exists,description_file_exists,name_exists, \
        descr_short_exists, descr_long_exists,licence_exists, ui_run))

    def read_json(self, path, filename):
        name = False
        descr_short = False
        descr_long = False
        licence = False
        filepath = f"{path}/{filename}"
        if os.stat(filepath).st_size > 0:
            file = open(filepath)
            content = json.load(file)
            if "name" in content and len(content["name"]) > 0:
                name = True
            if "descr_short" in content and len(content["descr_short"]) > 0:
                descr_short = True
            if "descr_long" in content and len(content["descr_long"]) > 0:
                descr_long = True
            if "licence" in content and len(content["licence"]) > 0:
                licence = True
            file.close()

        return (name,descr_short,descr_long,licence)
