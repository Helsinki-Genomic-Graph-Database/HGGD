import json

def check_file_extension(filename, extension):
    return filename.strip().split(".")[-1] == extension

def read_description(filepath):
    try:
        file = open(f"{filepath}/description.json")
    except:
        return None, None, None, None
    content = json.load(file)
    name = content["name"]
    descr_short = content["descr_short"]
    descr_long = content["descr_long"]
    licence = content["licence"]
    return (name, descr_short, descr_long, licence)
