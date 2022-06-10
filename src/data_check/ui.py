from datetime import datetime
from src.data_check.json_writer import JsonWriter
from src.data_check.validator import Validator
from src.data_check.zip_creator import ZipCreator

class UI:
    """This is a text-based user interface for processing
    the dataset so they're ready for the website.
    """
    def __init__(self, dataset_list, input_output):
        self.dataset_list = dataset_list
        self._io = input_output
        self._validator = Validator()
        self._writer = JsonWriter()
        self.something_updated = False

    def start(self):
        """This method goes through all the datasets in
        a loop and call the appropriate methods to
        check and add to the data.
        """
        for dataset in self.dataset_list:
            self.something_updated = False
            self._io.write("-------")
            self._io.write("Folder:")
            self._io.write(dataset.get_folder_name())
            self._io.write("Dataset:")
            if dataset.get_name() is None:
                self._io.write("(The dataset has no name)")
            else:
                self._io.write(dataset.get_name())
            if self._validator.check_show_on_website(dataset):
                print("Folder done.")
                continue
            data_exists = self.process_data(dataset)
            if not data_exists:
                continue
            json_path = self._writer.get_json_path(dataset)
            questions_asked = self.process_json_file(dataset, json_path)
            self.something_updated = questions_asked
            self.process_name(dataset)
            self.process_short_desc(dataset)
            self.process_long_description(dataset, questions_asked)
            self.process_licence(dataset, questions_asked)
            self.folder_done(dataset)

    def process_data(self, dataset):
        data_exists = self._validator.check_data_exists(dataset)
        if not data_exists:
            print_out = "\033[1;33;40mThere is no data in \
folder "+dataset.get_folder_name()+".\033[0;37;40m"
            self._io.write(print_out)
            self._io.write("Folder done.")
            return False
        self._io.write("\033[1;32;40mData exists.\033[0;37;40m")
        return True

    def process_json_file(self, dataset, json_path):
        questions_asked = False
        json_exists = self._validator.check_description_file_exists(dataset)
        if json_exists:
            json_empty = self._validator.check_description_file_empty(json_path)
        if not json_exists or json_empty:
            name = self.ask_name()
            sh_desc = self.ask_sh_desc()
            long_desc = self.ask_long_desc()
            licence = self.ask_for_licence()
            if len(licence) == 0:
                licence = "None"
            self._writer.create_json_file(dataset, name, sh_desc, long_desc, licence)
            dataset.set_name(name)
            dataset.set_descr_short(sh_desc)
            dataset.set_descr_long(long_desc)
            dataset.set_licence(licence)
            dataset.set_description_file_exists(True)
            questions_asked = True
        self._io.write("\033[1;32;40mJson-file exists.\033[0;37;40m")
        return questions_asked

    def process_name(self, dataset):
        name_exists = self._validator.check_name_exists(dataset)
        if not name_exists:
            name = self.ask_name()
            self._writer.update_json_file(dataset, "name", name)
            self.something_updated = True
        self._io.write("\033[1;32;40mName exists.\033[0;37;40m")

    def process_short_desc(self, dataset):
        short_desc_exists = self._validator.check_descr_short_exists(dataset)
        if not short_desc_exists:
            sh_desc = self.ask_sh_desc()
            self._writer.update_json_file(dataset, "descr_short", sh_desc)
            self.something_updated = True
        self._io.write("\033[1;32;40mShort description exists.\033[0;37;40m")

    def process_long_description(self, dataset, questions_asked):
        long_desc_exists = self._validator.check_descr_long_exists(dataset)
        long_desc = dataset.get_descr_long()
        if not questions_asked:
            if not long_desc_exists:
                long_desc = self.ask_long_desc()
                self._writer.update_json_file(dataset, "descr_long", long_desc)
                self.something_updated = True
        if long_desc == "":
            self._io.write("\033[1;33;40mYou chose that the dataset \
doesn't have a long description.\033[0;37;40m")
        else:
            self._io.write("\033[1;32;40mLong description exists.\033[0;37;40m")

    def process_licence(self, dataset, questions_asked):
        licence_exists = self._validator.check_licence_exists(dataset)
        print(licence_exists)
        licence = dataset.get_licence()
        if not questions_asked:
            if not licence_exists:
                licence = self.ask_for_licence()
                if licence == "":
                    licence = "None"
                if licence != "None":
                    self._writer.update_json_file(dataset, "licence", licence)
                    self.something_updated = True
        if licence == "None":
            self._io.write("\033[1;33;40mYou chose that the dataset \
doesn't have a licence.\033[0;37;40m")
        else:
            self._io.write("\033[1;32;40mLicence exists.\033[0;37;40m")

    def ask_name(self):
        name = ""
        while name == "":
            self._io.write("\033[1;31;40mThe dataset has no name.\033[0;37;40m")
            name = self._io.read("Please give a name: ")
        return name

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

    def ask_for_licence(self):
        self._io.write("\033[1;31;40mThe dataset has no licence.\033[0;37;40m")
        licence = self._io.read("Which licence is the dataset under? (Leave empty if no licence.) ")
        return licence

    def folder_done(self, dataset):
        """
        This method creates a log.txt file to save the date
        and time when the ui was last run and a zip-file for the
        dataset's graphs for the website.

        Args:
            dataset
        """
        if dataset.get_has_log_file() or self.something_updated:
            self._io.write("Data has been checked and updated.")
        else:
            self._io.write("Data has been checked.")
        self._io.write("Folder done.")
        path = dataset.get_path()
        name = dataset.get_folder_name()
        logstamp = datetime.now().isoformat(" ", "seconds")
        with open(path+"/log.txt", "w", encoding='utf-8') as log:
            log.write(f"ui run on: {logstamp}")
        zip_c = ZipCreator()
        zip_c.create_zip(name, path)
