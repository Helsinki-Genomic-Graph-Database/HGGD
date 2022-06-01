class FolderReaderMocK:
    def __init__(self):
        pass

    def get_folder_info(self):
        folder_list = []
        folder_list.append(("path_name1", True, True, True, True, True))
        folder_list.append(("path_name2", False, True, True, True, True))
        folder_list.append(("path_name3", True, False, False, False, False))
        folder_list.append(("path_name4", True, True, False, True, True))
        folder_list.append(("path_name5", True, True, True, False, True))
        folder_list.append(("path_name6", True, True, True, True, False))
        folder_list.append(("path_name7", True, True, True, True, False))
        return folder_list