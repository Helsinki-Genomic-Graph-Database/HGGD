import os
from datetime import datetime

def check_dataset_ui_run(datasetpath):
    if not os.path.exists(datasetpath+"/log.txt"):
        return False
    try:
        with open(datasetpath+"/log.txt") as log:
            line = log.readline()
            lo = get_datetime_from_log_text(line)
    except:
        return False

    res = True
    files = os.listdir(datasetpath)
    ltime = os.path.getctime(datasetpath+"/log.txt")
    
    for file in files:
        if not check_log_update_after_file_modified(datasetpath+"/"+file, ltime) and file != "log.txt":
            res = False

    return res

def check_log_update_after_file_modified(filepath, logtime):
    logtime = float(logtime)
    modified = os.path.getctime(filepath)
    return logtime >= modified

def get_datetime_from_log_text(log):
    logtime = log[11:].strip()
    return datetime.fromisoformat(logtime)