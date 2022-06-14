import os
import zipfile
import pathlib
from src.file_ui.file_utils import check_file_extension

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
                if check_file_extension(file, "zip"):
                    os.remove(f"{directory}/zip/{file}")
        directoryfiles = pathlib.Path(directory)
        if not os.path.exists(f"{directory}/zip"):
            os.mkdir(f"{directory}/zip")
        with zipfile.ZipFile(f"{directory}/zip/{filename}.zip", mode="w") as archive:
            for file_path in directoryfiles.iterdir():
                archive.write(file_path, arcname=file_path.name)
        return f"{filename}.zip"

zipcreator_service = ZipCreator()
