from os import getenv
from src.data_check.spdx_reader import SpdxReader

class SpdxService:
    def __init__(self):
        self.reader = SpdxReader()
        self.path = getenv("SPDX_FILE")
        self.identifier_list = self.set_identifier_list()

    def set_identifier_list(self):
        return self.reader.get_identifier_list_from_file(self.path)

    def get_identifier_list(self):
        return self.identifier_list

    def create_licence_link_tuples(self, licence):
        format = self.check_if_licence_in_spdx_format(licence)
        link_string = f"https://spdx.org/licenses/{licence}.html"
        if format is False:
            link_string = None
        licence_tuple = (licence, link_string)
        return licence_tuple

    def check_if_licence_in_spdx_format(self, licence):
        identifier_list = self.get_identifier_list()
        if licence in identifier_list:
            return True
        return False
