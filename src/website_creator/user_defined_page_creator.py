import os
from src.file_ui.file_utils import check_file_extension

class UserDefinedPageCreator:

    def __init__(self, user_defined_page_dir):
        self.user_defined_page_dir = user_defined_page_dir
        self.files = os.listdir(self.user_defined_page_dir)
        self.created_pages = []

    def get_pages(self):
        for file in self.files:
            if check_file_extension(file, "json"):
                self.created_pages.append(file)

        return self.created_pages
