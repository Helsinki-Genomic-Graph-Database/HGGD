import json

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
