from multiprocessing.spawn import import_main_path
import sys
org_path = sys.path[0]
modified_path = org_path[:-4]
sys.path[0] = modified_path
#to fix the import paths to work in the same way as they do with gunicorn

from src.entities.dataset import Dataset
from src.data_check.ui import UI
from src.data_check.console_io import ConsoleIO

def main():

    # dataset_test = Dataset(folder, description_file_exists,data_exists, licence_file_exists, path, name, descr_short, descr_long, licence, zipname, show_on_website)
    dataset1 = Dataset("folder_name1", True, True, True, "/home/smadetoj/Kurssit/ohtuprojekti/HGGD/data/Dataset1", "name1", "descr_short1", "descr_long1", "licence1", "zipname1", False)
    dataset2 = Dataset("folder_name2", True, False, False, "/home/smadetoj/Kurssit/ohtuprojekti/HGGD/data/Dataset2", None, None, None, None, "zipname2", False)
    dataset3 = Dataset("folder_name3", False, True, False,  "/home/smadetoj/Kurssit/ohtuprojekti/HGGD/data/Dataset3", None, None, None, None, "zipname3", False)
    dataset4 = Dataset("folder_name4", True,True, False, "/home/smadetoj/Kurssit/ohtuprojekti/HGGD/data/Dataset4", None, "descr_short", "descr_long", "licence", "zipname", False)
    dataset5 = Dataset("folder_name5", True,True, False, "/home/smadetoj/Kurssit/ohtuprojekti/HGGD/data/Dataset5", "name", None, "descr_long", "licence", "zipname", False)
    dataset6 = Dataset("folder_name6", True,True, False, "/home/smadetoj/Kurssit/ohtuprojekti/HGGD/data/Dataset6", "name", "descr_short", None, "licence", "zipname", False)
    dataset7 = Dataset("folder_name7", True,True, False, "/home/smadetoj/Kurssit/ohtuprojekti/HGGD/data/Dataset7", "name", "descr_short", "descr_long", None, "zipname", False)
    # dataset8 = Dataset(True,True, False, "/home/smadetoj/Kurssit/ohtuprojekti/HGGD/data/Dataset8", "name", "descr_short", "descr_long", "licence", "zipname", False)
    dataset_list = [dataset1, dataset2, dataset3, dataset4, dataset5, dataset6, dataset7]
    # DC = DatasetCreator
    # dataset_list = DC.get_dataset_list()
    input_output = ConsoleIO()
    ui = UI(dataset_list, input_output)
    ui.start()

if __name__ == "__main__":
    main()
