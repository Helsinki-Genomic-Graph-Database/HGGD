import os
import zipfile
import pathlib

class ZipCreator:
    """ Makes a zipfile for a dataset of graphs
    """
    def __init__(self):
        pass

    def create_zip(self, filename, directory):
        """ Checks if a zipfile exists in the datafolder
        If not, it makes one for the dataset files

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
        directoryfiles = pathlib.Path(directory)
        if not os.path.exists(f"{directory}/zip"):
            os.mkdir(f"{directory}/zip")
        with zipfile.ZipFile(f"{directory}/zip/{filename}.zip", mode="w") as archive:
            for file_path in directoryfiles.iterdir():
                archive.write(file_path, arcname=file_path.name)
        return f"{filename}.zip"

    def check_file_extension(self, filename, extension):
        return filename.strip().split(".")[-1] == extension

zipcreator_service = ZipCreator()
