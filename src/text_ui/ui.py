import os
import json


class UI:
    def __init__(self, folder_reader, input_output):
        self.folder_reader = folder_reader
        self._io = input_output

    def start(self):
        folder_list = self.folder_reader.get_folder_info()
        for folder in folder_list:
            self._io.write("-------")
            self._io.write("Folder:")
            folder_name, data_exists, json_exists, name_exists, short_desc_exists, \
            long_desc_exists, licence_exists = folder[:-1] # skips info on whether there are modifications after ui run for now
            self._io.write(folder_name)
            self.process_data(folder_name, data_exists)
            if not data_exists:
                continue
            json_path = folder_name+"/description.json"
            json_empty = os.stat(json_path).st_size == 0
            self.process_json_file(json_exists, json_path, json_empty)
            if not json_exists or json_empty:
                self._io.write("Folder done.")
                continue
            self.process_name(name_exists, json_path)
            self.process_short_desc(short_desc_exists, json_path)
            self.process_long_description(long_desc_exists, json_path)
            self.process_licence(licence_exists, json_path)
            self._io.write("Folder done.")

    def process_data(self, folder_name, data_exists):
        if not data_exists:
            print_out = "\033[1;33;40mThere is not data in folder "+folder_name+".\033[0;37;40m"
            self._io.write(print_out)
            self._io.write("Folder done.")
        else:
            self._io.write("\033[1;32;40mData exists.\033[0;37;40m")

    def process_json_file(self, json_exists, json_path, json_empty):
        if not json_exists or json_empty:
            name = self.ask_name()
            sh_desc = self.ask_sh_desc()
            long_desc = self.ask_long_desc()
            licence = self.ask_for_licence()
            self.create_json_file(json_path, name, sh_desc, long_desc, licence)
            self._io.write("\033[1;32;40mJson-file exists.\033[0;37;40m")
            self._io.write("\033[1;32;40mName exists.\033[0;37;40m")
            self._io.write("\033[1;32;40mShort description exists.\033[0;37;40m")
            if long_desc == "":
                self._io.write("\033[1;33;40mYou chose that the dataset \
doesn't have a long description.\033[1;37;40m")
            else:
                self._io.write("\033[1;32;40mLong description exists.\033[0;37;40m")
            if licence == "":
                self._io.write("\033[1;33;40mYou chose that the dataset \
doesn't have a licence.\033[0;37;40m")
            else:
                self._io.write("\033[1;32;40mLicence exists.\033[0;37;40m")
        else:
            self._io.write("\033[1;32;40mJson-file exists.\033[0;37;40m")

    def process_name(self, name_exists, json_path):
        if not name_exists:
            name = self.ask_name()
            self.update_json_file(json_path, "name", name)
        self._io.write("\033[1;32;40mName exists.\033[0;37;40m")

    def process_short_desc(self, short_desc_exists, json_path):
        if not short_desc_exists:
            sh_desc = self.ask_sh_desc()
            self.update_json_file(json_path, "descr_short", sh_desc)
        self._io.write("\033[1;32;40mShort description exists.\033[0;37;40m")

    def process_long_description(self, long_desc_exists, json_path):
        if not long_desc_exists:
            long_desc = self.ask_long_desc()
            self.update_json_file(json_path, "descr_long", long_desc)
            if long_desc == "":
                self._io.write("\033[1;33;40mYou chose that the dataset \
doesn't have a long description.\033[0;37;40m")
            else:
                self._io.write("\033[1;32;40mLong description exists.\033[0;37;40m")
        else:
            self._io.write("\033[1;32;40mLong description exists.\033[0;37;40m")

    def process_licence(self, licence_exists, json_path):
        if not licence_exists:
            licence = self.ask_for_licence()
            if len(licence)==0:
                licence = "None"
            self.update_json_file(json_path, "licence", licence)
            if licence == "None":
                self._io.write("\033[1;33;40mYou chose that the dataset \
doesn't have a licence.\033[0;37;40m")
            else:
                self._io.write("\033[1;32;40mLicence exists.\033[0;37;40m")
        else:
            self._io.write("\033[1;32;40mLicence exists.\033[0;37;40m")

    def ask_name(self):
        name = ""
        while name == "":
            self._io.write("\033[1;31;40mThe dataset has no name.\033[0;37;40m")
            name = self._io.read("Please give a name: ")
        return name

    def ask_for_licence(self):
        self._io.write("\033[1;31;40mThe dataset has no licence.\033[0;37;40m")
        licence = self._io.read("Which licence is the dataset under? (Leave empty if no licence.) ")
        return licence

    def ask_sh_desc(self):
        sh_desc = ""
        while sh_desc == "":
            self._io.write("\033[1;31;40mThe dataset doesn't \
have a short description.\033[0;37;40m")
            sh_desc = self._io.read("Please give a short description: ")
        return sh_desc

    def ask_long_desc(self):
        self._io.write("\033[1;31;40mThe dataset doesn't have a long description.\033[0;37;40m")
        long_desc = self._io.read("Please give a long description or leave empty: ")
        return long_desc

    def create_json_file(self, json_path, name, sh_desc, long_desc, licence):
        dataset_dict = {
            "name" : name,
            "descr_short" : sh_desc,
            "descr_long" : long_desc,
            "licence" : licence
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
