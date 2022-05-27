import sys
org_path = sys.path[0]
modified_path = org_path[:-4]
sys.path[0] = modified_path

from src.file_ui.dataset_reader import DatasetReader
from src.file_ui.folder_reader import FolderReader
from src.text_ui.ui import UI

def main():

    reader = DatasetReader("data")
    f_reader = FolderReader(reader.get_paths())
    ui = UI(f_reader)
    ui.start()

if __name__ == "__main__":
    main()
