from bs4 import BeautifulSoup as bs
import requests

class SpdxReader:
    def __init__(self):
        self.url = "https://spdx.org/licenses/"

    def check_access(self):
        return requests.get(self.url)

    def fetch_spdx_identifiers_in_html(self):
        page = self.check_access()
        if not page.status_code == 200:
            return None
        soup = bs(page.content, features="html.parser")
        return soup.find_all(property="spdx:licenseId")

    def list_spdx_identifiers(self):
        html_id_list = self.fetch_spdx_identifiers_in_html()
        if html_id_list is None:
            return None
        identifiers = [id.text for id in html_id_list]
        return identifiers

    def get_identifier_list_from_website(self):
        identifier_list = self.list_spdx_identifiers()
        return identifier_list

    def write_spdx_identifier_file(self, identifier_list, path):
        if not identifier_list is None:
            file = open(path, "w", encoding="utf_8")
            for identifier in identifier_list:
                file.write(identifier)
                file.write("\n")
            file.close()

    def read_spdx_identifier_file(self, path):
        identifier_list = []
        try:
            file = open(path, "r", encoding="utf_8")
            for line in file:
                line = line.strip("\n")
                identifier_list.append(line)
            file.close()
        except:
            identifier_list = None
        return identifier_list

    def get_identifier_list_from_file(self, path):
        identifier_list = self.read_spdx_identifier_file(path)
        return identifier_list
