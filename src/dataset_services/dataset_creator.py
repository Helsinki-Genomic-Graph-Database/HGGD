from src.dataset_services.folder_reader import FolderReader

class DatasetCreator:
    """Gets a list of folder paths, calls folder reader for each of them,
    and returns a list of dataset objects created from the folders
    """

    def __init__(self, folder_paths, spdx_service):
        self.folder_paths = folder_paths
        self.dataset_list = []
        self.spdx_service = spdx_service

    def get_datasets(self):
        self.run()
        return sorted(self.dataset_list)

    def get_datasets_to_show_on_website(self):
        self.run(True)
        return sorted(self.dataset_list)

    def run(self, for_website = False):
        for path in self.folder_paths:
            folder_reader = FolderReader(path, self.spdx_service)
            if for_website:
                dataset = folder_reader.get_dataset()
                if dataset.get_show_on_website():
                    self.dataset_list.append(dataset)
            else:
                self.dataset_list.append(folder_reader.get_dataset())

