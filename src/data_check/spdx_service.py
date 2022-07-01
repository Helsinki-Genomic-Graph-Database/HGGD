from os import getenv
from src.data_check.spdx_reader import SpdxReader

class SpdxService:
    """This class set and gets SPDX identifier list
    for other classes to use. It also creates link tuples
    and checks whether licence is in SPDX format.
    """
    def __init__(self):
        self.reader = SpdxReader()
        self.path = getenv("SPDX_FILE")
        self.identifier_list = self.set_identifier_list()

    def set_identifier_list(self):
        new_list = self.reader.get_identifier_list_from_website()
        if not new_list is None:
            self.reader.write_spdx_identifier_file(new_list, self.path)
            return new_list
        return self.reader.get_identifier_list_from_file(self.path)

    def get_identifier_list(self):
        return self.identifier_list

    def create_licence_link_tuples(self, licence):
        """
        Returns:
            tuple: first item is licence (string) and
            second item is link (string) or None
        """
        spdx_format = self.check_if_licence_in_spdx_format(licence)
        link_string = f"https://spdx.org/licenses/{licence}.html"
        if spdx_format is False:
            link_string = None
        licence_tuple = (licence, link_string)
        return licence_tuple

    def check_if_licence_in_spdx_format(self, licence):
        identifier_list = self.get_identifier_list()
        if licence in identifier_list:
            return True
        return False
