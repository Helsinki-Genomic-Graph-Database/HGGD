import os

class Validator:
    def __init__(self):
        pass

    def check_description_file_exists(self, dataset):
        return dataset.get_description_file_exists()

    def check_data_exists(self, dataset):
        return dataset.get_data_exists()

    def check_licence_file_exists(self, dataset):
        return dataset.get_licence_file_exists()

    def check_name_exists(self, dataset):
        if (dataset.get_name()) == 0:
            return False
        if (dataset.get_name()) == None:
            return False
        return True

    def check_descr_short_exists(self, dataset):
        if (dataset.get_descr_short()) == 0:
            return False
        if (dataset.get_descr_short()) == None:
            return False
        return True

    def check_descr_long_exists(self, dataset):
        if (dataset.get_descr_long()) == 0:
            return False
        if (dataset.get_descr_long()) == None:
            return False
        return True

    def check_licence_exists(self, dataset):
        if (dataset.get_licence()) == 0:
            return False
        if (dataset.get_licence()) == None:
            return False
        return True

    def check_show_on_website(self, dataset):
        return dataset.get_show_on_website()

    def check_description_file_empty(self, json_path):
        return os.stat(json_path).st_size == 0
