import json
from src.file_ui.folder_reader import FolderReader


class UI:
    def __init__(self):
        self.folder_reader = FolderReader()

    def start(self):
        print("start")
        folder_list = self.folder_reader.get_folder_info()
        for folder in folder_list:
            print("-------")
            print("Folder:")
            folder_name, data_exists, json_exists, name_exists, short_desc_exists, long_desc_exists \
                = folder
            print(folder_name)
            if not data_exists:
                print("\033[1;33;40mThere is not data in folder", folder_name, ".\033[0;37;40m")
                print("Folder done.")
                continue
            else:
                print("\033[1;32;40mData exists.\033[0;37;40m")
            if not json_exists:
                name = self.ask_name()
                sh_desc = self.ask_sh_desc()
                long_desc = self.ask_long_desc()
                self.create_json_file(folder_name, name, sh_desc, long_desc)
                print("\033[1;32;40mJson-file exists.\033[0;37;40m")
                print("\033[1;32;40mName exists.\033[0;37;40m")
                print("\033[1;32;40mShort description exists.\033[0;37;40m")
                if long_desc == "":
                    print("\033[1;33;40mYou chose that the folder doesn't have a long description.\033[0;37;40m")
                else:
                    print("\033[1;32;40mLong description exists.\033[0;37;40m")
                continue
            print("\033[1;32;40mJson-file exists.\033[0;37;40m")
            if not name_exists:
                name = self.ask_name()
                self.update_json_file(folder_name, "name", name)
            print("\033[1;32;40mName exists.\033[0;37;40m")
            if not short_desc_exists:
                sh_desc = self.ask_sh_desc()
                self.update_json_file(folder_name, "descr_short", sh_desc)
            print("\033[1;32;40mShort description exists.\033[0;37;40m")
            if not long_desc_exists:
                long_desc = self.ask_long_desc()
                self.update_json_file(folder_name, "descr_long", long_desc)
                if long_desc == "":
                    print("\033[1;33;40mYou chose that the folder doesn't have a long description.\033[0;37;40m")
                else:
                    print("\033[1;32;40mLong description exists.\033[0;37;40m")
            else:
                print("\033[1;32;40mLong description exists.\033[0;37;40m")
            print("Folder done.")

    def ask_name(self):
        name = ""
        while name == "":
            print("\033[1;31;40mThe dataset has no name.\033[0;37;40m")
            name = input("Please give a name: ")
        return name

    def ask_sh_desc(self):
        sh_desc = ""
        while sh_desc == "":
            print("\033[1;31;40mThe folder doesn't have a short description.\033[0;37;40m")
            sh_desc = input("Please give a short description: ")
        return sh_desc

    def ask_long_desc(self):
        print("\033[1;31;40mThe folder doesn't have a long description.\033[0;37;40m")
        long_desc = input("Please give a long description or leave empty: ")
        return long_desc

    def create_json_file(self, folder_name, name, sh_desc, long_desc):
        dataset_dict = {
            "name" : name,
            "descr_short" : sh_desc,
            "descr_long" : long_desc
        }

        path_name = folder_name+"description.json"

        with open (path_name, "w") as file:
            json.dump(dataset_dict, file)

    def update_json_file(self, folder_name, key, value):
        new_info = {key : value}
        path_name = folder_name+"description.json"
        with open(path_name, "r+") as file:
            data = json.load(file)
            data.update(new_info)
            file.seek(0)
            json.dump(data, file)
