import sys
import json
import os
from json.decoder import JSONDecodeError

def check_file_extension(filename, extension):
    res = filename.strip().split(".")
    if len(res) < 2:
        return False
    return res[-1] == extension

def check_file_extension_multiple(filename, extension_list):
    found = False
    for extension in extension_list:
        if check_file_extension(filename, extension):
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
    return filename[:-len(extension)]

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
    sources = []
    if os.stat(filepath).st_size > 0:
        with open(filepath, encoding='utf-8') as file:
            try:
                content = json.load(file)
                name = check_field(content, "name")
                descr_short = check_field(content, "descr_short")
                descr_long = check_field(content, "descr_long")
                licence = check_field(content, "licence")
                user_defined_columns = check_field(content, "user_defined_columns")
                source_list = check_field(content, "sources")
                if source_list is not None:
                    for source in source_list:
                        sources.append((source, source))
            except JSONDecodeError as error:
                print(f"There was an error in the file: {filepath}")
                print("  ", error)
                sys.exit("Please fix the description file and start the program again.")

    return name, descr_short, descr_long, licence, user_defined_columns, sources

def read_graph_description(directory, name):
    """ Reads graph description files

    Args:
        directory (str): directory of the file
        name (str): filename without extension
    """
    filename = name + "_description.json"
    filepath = directory +"/"+ filename
    name = None
    licence = None
    short_desc = None
    sources = []
    user_defined_columns = None
    if os.stat(filepath).st_size > 0:
        with open(filepath, encoding='utf-8') as file:
            try:
                content = json.loads(file.read())
                name = check_field(content, "name")
                licence = check_field(content, "licence")
                source_list = check_field(content, "sources")
                short_desc = check_field(content, "descr_short")
                user_defined_columns = check_field(content, "user_defined_columns")
                if source_list is not None:
                    for source in source_list:
                        sources.append((source, source))
            except JSONDecodeError as error:
                print(f"There was an error in the file: {filepath}")
                print("  ", error)
                sys.exit("Please fix the description file and start the program again.")
    return name, licence, sources, short_desc, user_defined_columns

def check_description_file_exists(directory, filename):
    """ Checks if there is a description file
    for the graph

    Args:
        directory (str): directory of the file
        name (str): filename without extension

    Returns:
        boolean: if the file exists
    """
    json_name = filename+"_description.json"
    return os.path.exists(os.path.join(directory, json_name))

def create_source_txt_file(directory, filename_without_extension, sourcelist, graph=True):
    target_directory = f"{directory}/sourcetxt"
    if not os.path.exists(target_directory):
        os.mkdir(target_directory)
    if graph:
        target_directory = f"{target_directory}/graphs"
        if not os.path.exists(target_directory):
            os.mkdir(target_directory)
    txt_filename = filename_without_extension+".txt"
    new_sourcelist = []
    for source in sourcelist:
        new_sourcelist.append(source[0])
    with open (f"{target_directory}/{txt_filename}", "w", encoding='utf-8') as file:
        file.write("\n".join(new_sourcelist))
