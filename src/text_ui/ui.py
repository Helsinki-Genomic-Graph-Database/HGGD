import os
import json


class UI:
    def __init__(self, folder_reader, io):
        self.folder_reader = folder_reader
        self._io = io

    def start(self):
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
            print("\033[1;32;40mData exists.\033[0;37;40m")
            json_path = folder_name+"/description.json"
            if not json_exists or os.stat(json_path).st_size == 0:
                name = self.ask_name()
                sh_desc = self.ask_sh_desc()
                long_desc = self.ask_long_desc()
                self.create_json_file(json_path, name, sh_desc, long_desc)
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
                self.update_json_file(json_path, "name", name)
            print("\033[1;32;40mName exists.\033[0;37;40m")
            if not short_desc_exists:
                sh_desc = self.ask_sh_desc()
                self.update_json_file(json_path, "descr_short", sh_desc)
            print("\033[1;32;40mShort description exists.\033[0;37;40m")
            if not long_desc_exists:
                long_desc = self.ask_long_desc()
                self.update_json_file(json_path, "descr_long", long_desc)
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
            name = self._io.read("Please give a name: ")
        return name

    def ask_sh_desc(self):
        sh_desc = ""
        while sh_desc == "":
            print("\033[1;31;40mThe folder doesn't have a short description.\033[0;37;40m")
            sh_desc = self._io.read("Please give a short description: ")
        return sh_desc

    def ask_long_desc(self):
        print("\033[1;31;40mThe folder doesn't have a long description.\033[0;37;40m")
        long_desc = self._io.read("Please give a long description or leave empty: ")
        return long_desc

    def create_json_file(self, json_path, name, sh_desc, long_desc):
        dataset_dict = {
            "name" : name,
            "descr_short" : sh_desc,
            "descr_long" : long_desc
        }

        with open (json_path, "w") as file:
            json.dump(dataset_dict, file)

    def update_json_file(self, json_path, key, value):
        new_info = {key : value}
        with open(json_path, "r+") as file:
            data = json.load(file)
            data.update(new_info)
            file.seek(0)
            json.dump(data, file)
