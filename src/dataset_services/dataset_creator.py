from src.dataset_services.folder_reader import FolderReader

class DatasetCreator:
    """Gets a list of folder paths, calls folder reader for each of them,
    and returns a list of dataset objects created from the folders
    """

    def __init__(self, folder_paths):
        self.folder_paths = folder_paths
        self.dataset_list = []

    def get_datasets(self):
        self.run()
        return sorted(self.dataset_list)

    def run(self):
        for path in self.folder_paths:
            folder_reader = FolderReader(path)
            self.dataset_list.append(folder_reader.get_dataset())
