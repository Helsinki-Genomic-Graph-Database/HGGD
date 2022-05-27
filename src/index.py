import sys
org_path = sys.path[0]
modified_path = org_path[:-4]
sys.path[0] = modified_path

from src.file_ui.dataset_reader import DatasetReader
from src.file_ui.folder_reader import FolderReader

def main():

    reader = DatasetReader("src/tests/testdata_for_dataset_reader")
    
    f_reader = FolderReader(reader.get_paths())
    print(f_reader.get_folder_info())

if __name__ == "__main__":
    main()
