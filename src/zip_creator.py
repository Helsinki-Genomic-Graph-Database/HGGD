import shutil
import os

class ZipCreator:
    """ Makes a zipfile for a dataset of graphs
    """
    def __init__(self):
        pass

    def create_zip(self, filename, directory):
        """ Checks if a zipfile exists in the datafolder
        If not, it makes one for the dataset

        Args:
            filename (str): Name of the dataset and zipfile
            directory (str): directory path

        Returns:
            str: zipfile name
        """
        if os.path.exists(f"{directory}/zip"):
            files = os.listdir(f"{directory}/zip")
            for file in files:
                if self.check_file_extension(file, "zip"):
                    return file
        shutil.make_archive(f"./data/zip/{filename}", 'zip', directory)
        return f"{filename}.zip"

    def check_file_extension(self, filename, extension):
        return filename.strip().split(".")[-1] == extension

zipcreator_service = ZipCreator()
