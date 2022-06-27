from os import getenv
import sys
from dotenv import load_dotenv
org_path = sys.path[0]
modified_path = org_path[:-4]
sys.path[0] = modified_path
#to fix the import paths to work in the same way as they do with gunicorn

load_dotenv()

from src.dataset_services.dataset_reader import DatasetReader
from src.dataset_services.dataset_creator import DatasetCreator
from src.data_check.ui import UI
from src.data_check.console_io import ConsoleIO
from src.data_check.spdx_service import SpdxService

def main():

    data_directory = getenv("DIR")
    spdx_service = SpdxService()
    reader = DatasetReader(data_directory)
    dir_paths = reader.get_paths()
    creator = DatasetCreator(dir_paths, spdx_service)
    dataset_list = creator.get_datasets()
    input_output = ConsoleIO()
    user_interface = UI(dataset_list, input_output, spdx_service)
    user_interface.start()

if __name__ == "__main__":
    main()
