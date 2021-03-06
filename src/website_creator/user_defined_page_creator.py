import os
import json
from src.file_ui.file_utils import check_file_extension, check_field, remove_file_extension

class UserDefinedPageCreator:

    def __init__(self, user_defined_page_dir):
        self.user_defined_page_dir = user_defined_page_dir
        self.files = os.listdir(self.user_defined_page_dir)
        self.created_pages = {}
        if not os.path.exists(f"{self.user_defined_page_dir}/pages"):
            os.mkdir(f"{self.user_defined_page_dir}/pages")
        self.run()

    def run(self):
        for file in self.files:
            if check_file_extension(file, "json"):
                with open(self.user_defined_page_dir+"/"+file) as jsonfile:
                    content = json.load(jsonfile)
                    name = check_field(content, "name")
                    page_content = check_field(content, "content")
                    file_wo_extension = remove_file_extension(file, "json")[:-1]
                    path = self.user_defined_page_dir+"/pages/"+file_wo_extension+".html"
                self.write_html(path, page_content, name)
                file_wo_extension = remove_file_extension(file, "json")[:-1]
                self.created_pages[file_wo_extension] = name

    def get_pages(self):
        return self.created_pages

    def write_html(self, url, page_content, name):
        with open(url, "w") as html:
            html.write('{% extends "layout.html" %}\n\n')
            html.write('{% block title %}\n'+name+'\n{% endblock %}\n\n')
            html.write('{% block body %}\n')
            html.write('<hy-docs-container>\n')
            html.write('<hy-paragraph-text>\n')
            html.write(page_content)
            html.write('\n</hy-paragraph-text>')
            html.write('\n</hy-docs-container>')
            html.write('\n{% endblock %}')

    def get_page_names(self):
        # create list of tuples: (link ending, page name)
        names = []
        for key in sorted(self.created_pages.keys()):
            names.append((key, self.created_pages[key]))
        return names
