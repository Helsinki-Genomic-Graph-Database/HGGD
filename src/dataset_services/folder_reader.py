import os
import json
from src.file_ui.file_utils import check_file_extension, check_file_extension_multiple, check_field, read_description
from src.entities.dataset import Dataset

class FolderReader:

    """
    Reads a folder and makes a Dataset object from the contents
    """

    def __init__(self, path):

        self.path = path
        self.files = os.listdir(path)
        self.descrition_file_exists = False
        self.data_exists = False
        self.licence_file_exists = False
        self.name = None
        self.descr_short = None
        self.descr_long = None
        self.licence = []
        self.user_defined_columns = None
        self.show_on_website = False
        self.folder_name = path.split("/")[-1]
        self.highest_modification_time = 0
        self.logtime = 0
        self.has_log_file = False
        self.graph_info = []

    def get_dataset(self):
        graphs = []
        graph_descriptions = []
        for file in self.files:
            self.check_modification_times(file)

            if check_file_extension_multiple(file, ["graph", "gfa", "dimacs"]):
                self.data_exists = True
                graphs.append(file)

            if check_file_extension(file, "json"):
                if file == "description.json":
                    self.descrition_file_exists = True
                    self.name, self.descr_short, self.descr_long, licence_in_descr, self.user_defined_columns = read_description(self.path)
                    if licence_in_descr:
                        self.licence.append(licence_in_descr)
                else:
                    split_file = file.split(".")[:-1]
                    if (split_file[-1].split("_")[-1]) == "description":
                        graph_descriptions.append(file[:-len("_description.json")])


            if check_file_extension(file, "licence"):
                self.licence_file_exists = True

        ui_run = (self.logtime >= self.highest_modification_time)

        if ui_run and self.data_exists:
            self.show_on_website = True

        for graph in graphs:
            has_licence = False
            if check_file_extension(graph, "graph"):
                has_licence = True
            else:
                if graph in graph_descriptions:
                    filepath = self.path+"/"+graph+"_description.json"
                    if os.stat(filepath).st_size > 0:
                        with open(filepath, encoding='utf-8') as file:
                            content = json.load(file)
                            if check_field(content, "licence") is not None:
                                has_licence = True

            self.graph_info.append((graph, has_licence))

        return Dataset(self.descrition_file_exists, self.data_exists, self.licence_file_exists, \
                self.path, self.name, self.descr_short, self.descr_long, self.licence, \
                self.show_on_website, self.folder_name, self.user_defined_columns, \
                self.has_log_file, self.graph_info)

    def check_modification_times(self, file):
        modification_time = os.path.getctime(self.path+"/"+file)
        if file == "log.txt":
            self.logtime = modification_time
            self.has_log_file = True
        else:
            if modification_time > self.highest_modification_time:
                self.highest_modification_time = modification_time

    # def read_description(self, path):
    #     filepath = path+"/description.json"
    #     name = None
    #     descr_short = None
    #     descr_long = None
    #     licence = None
    #     user_defined_columns = None
    #     if os.stat(filepath).st_size > 0:
    #         with open(filepath, encoding='utf-8') as file:
    #             content = json.load(file)
    #             name = self.check_field(content, "name")
    #             descr_short = self.check_field(content, "descr_short")
    #             descr_long = self.check_field(content, "descr_long")
    #             licence = self.check_field(content, "licence")
    #             user_defined_columns = self.check_field(content, "user_defined_columns")

    #     return name, descr_short, descr_long, licence, user_defined_columns

    # def check_field(self, content, field):
    #     if field in content and len(content[field]) > 0:
    #         if field == "user_defined_columns":
    #             return self.handle_user_defined_columns(content[field])
    #         return content[field]

    #     return None

    # def handle_user_defined_columns(self, user_defined_columns):
    #     column_list = []
    #     for name, content in user_defined_columns.items():
    #         column_list.append((name, content))
    #     return column_list
