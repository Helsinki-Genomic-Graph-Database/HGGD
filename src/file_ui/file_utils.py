import json
import os

def check_file_extension(filename, extension):
    return filename.strip().split(".")[-1] == extension

def check_file_extension_multiple(filename, extension_list):
    found = False
    for extension in extension_list:
        if filename.strip().split(".")[-1] == extension:
            found = True
    return found

def read_licence_files(filepath, filename, graph):
    try:
        licence_file = open(f"{filepath}/{filename}", encoding='utf-8')
    except:
        return False
    content = licence_file.readlines()
    licence_file.close()
    for graph_name in content:
        graph_name = graph_name.strip()
        if graph_name == graph.get_names():
            return True
    return False

def read_licence_names_from_files(filepath):
    file_list = list_licence_files(filepath)
    licence_list = []
    for filename in file_list:
        filename = filename.strip(".licence")
        licence_list.append(filename)
    licence_string = str(licence_list[0])
    for licence in licence_list:
        if str(licence)is not licence_string:
            licence_string = licence_string+", "+licence
    return licence_string

def list_licence_files(path):
    files = os.listdir(path)
    file_list = []
    for filename in files:
        if check_file_extension(filename, "licence"):
            file_list.append(filename)
    return file_list

def remove_file_extension(filename, extension):
    ext_letter_amount = len(extension)
    filename_letter_amount = len(filename)
    difference = filename_letter_amount - ext_letter_amount
    filename = filename[0:difference]
    return filename

def check_field(content, field):
        if field in content and len(content[field]) > 0:
            if field == "user_defined_columns":
                return handle_user_defined_columns(content[field])
            return content[field]

        return None

def handle_user_defined_columns(user_defined_columns):
    column_list = []
    for name, content in user_defined_columns.items():
        column_list.append((name, content))
    return column_list

def read_description(path):
        filepath = path+"/description.json"
        name = None
        descr_short = None
        descr_long = None
        licence = None
        user_defined_columns = None
        if os.stat(filepath).st_size > 0:
            with open(filepath, encoding='utf-8') as file:
                content = json.load(file)
                name = check_field(content, "name")
                descr_short = check_field(content, "descr_short")
                descr_long = check_field(content, "descr_long")
                licence = check_field(content, "licence")
                user_defined_columns = check_field(content, "user_defined_columns")

        return name, descr_short, descr_long, licence, user_defined_columns
