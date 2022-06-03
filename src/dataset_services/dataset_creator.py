import os
import json
from src.entities.dataset import Dataset
from src.file_ui.file_utils import check_file_extension

class DatasetCreator:

    def __init__(self, folder_paths):
        self.folder_paths = folder_paths
        self.dataset_list = []

    def get_datasets(self):
        self.run()
        return self.dataset_list

    def run(self):
        for path in self.folder_paths:
            files = os.listdir(path)
            descrition_file_exists = False
            data_exists = False
            licence_file_exists = False
            path = path
            name = None
            descr_short = None
            descr_long = None
            licence = None
            zipname = path+"/zip"
            show_on_website = False
            folder_name = path.split("/")[-1]
            highest_modification_time = 0
            logtime =0
            for file in files:

                modification_time = os.path.getctime(path+"/"+file)
                if file == "log.txt":
                    logtime = modification_time
                else:
                    if modification_time > highest_modification_time:
                        highest_modification_time = modification_time

                if file == "description.json":
                    descrition_file_exists = True
                    name, descr_short, descr_long, licence = self.read_description(path)
                
                if check_file_extension(file, "graph"):
                    data_exists = True

                if check_file_extension(file, "licence"):
                    licence_file_exists = True

            ui_run = logtime >= highest_modification_time
            if ui_run and data_exists:
                show_on_website = True

            self.dataset_list.append(Dataset(descrition_file_exists, data_exists, licence_file_exists, \
                                            path, name, descr_short, descr_long, licence, zipname,\
                                             show_on_website, folder_name))

    def read_description(self, path):
        filepath = path+"/description.json"
        name = None
        descr_short = None
        descr_long = None
        licence = None
        if os.stat(filepath).st_size > 0:
            with open(filepath) as file:            
                content = json.load(file)
                name = self.check_field(content, "name")
                descr_short = self.check_field(content, "descr_short")
                descr_long = self.check_field(content, "descr_long")
                licence = self.check_field(content, "licence")
                
        return name, descr_short, descr_long, licence

    def check_field(self, content, field):
        if field in content and len(content[field]) > 0:
            return content[field]

        return None