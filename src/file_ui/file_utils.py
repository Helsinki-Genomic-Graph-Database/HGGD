import json
import os

def check_file_extension(filename, extension):
    return filename.strip().split(".")[-1] == extension

def read_description(filepath):
    try:
        file = open(f"{filepath}/description.json")
    except:
        return None, None, None, None
    content = json.load(file)
    try:
        name = content["name"]
    except:
        name = "No name (this should never happen)"
    try:
        descr_short = content["descr_short"]
    except:
        descr_short = "No short description (this should never happen)"
    try:
        descr_long = content["descr_long"]
    except:
        descr_long = ""
    try:
        licence = content["licence"]
    except:
        licence = "None"
    return (name, descr_short, descr_long, licence)

def read_licence_files(filepath, filename, graph):
    try:
        licence_file = open(f"{filepath}/{filename}")
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