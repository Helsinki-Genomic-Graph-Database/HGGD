from multiprocessing.spawn import import_main_path
import sys
org_path = sys.path[0]
modified_path = org_path[:-4]
sys.path[0] = modified_path
#to fix the import paths to work in the same way as they do with gunicorn

from src.dataset_services.dataset_reader import DatasetReader
from src.dataset_services.dataset_creator import DatasetCreator
from src.data_check.ui import UI
from src.data_check.console_io import ConsoleIO

def main():

    DIR = "data"
    DR = DatasetReader(DIR)
    dir_paths = DR.get_paths()
    DC = DatasetCreator(dir_paths)
    dataset_list = DC.get_datasets()
    input_output = ConsoleIO()
    ui = UI(dataset_list, input_output)
    ui.start()

if __name__ == "__main__":
    main()
