import sys
org_path = sys.path[0]
modified_path = org_path[:-4]
sys.path[0] = modified_path
#to fix the import paths to work in the same way as they do with gunicorn

from src.file_ui.dataset_reader import DatasetReader
from src.file_ui.folder_reader import FolderReader
from src.text_ui.ui import UI
from src.text_ui.console_io import ConsoleIO

def main():

    reader = DatasetReader("data")
    f_reader = FolderReader(reader.get_paths())
    io = ConsoleIO()
    ui = UI(f_reader, io)
    ui.start()

if __name__ == "__main__":
    main()
