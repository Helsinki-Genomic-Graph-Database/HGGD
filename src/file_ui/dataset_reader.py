import os

class DatasetReader:
    """
    give data dir as argument, returns paths to subdirectories as a list
    """

    def __init__(self, dirpath):
        self.dirpath = dirpath
        self.list_of_paths = []

    def get_paths(self):
        self.run()
        return self.list_of_paths

    def run(self):
        for path in os.listdir(self.dirpath):
            full_path = os.path.join(self.dirpath, path)
            if os.path.isdir(full_path):
                self.list_of_paths.append(full_path)
