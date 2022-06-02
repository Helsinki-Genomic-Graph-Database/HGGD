import os

def check_dataset_ui_run(datasetpath):
    if not os.path.exists(datasetpath+"/log.txt"):
        return False

    files = os.listdir(datasetpath)
    logtime = os.path.getctime(datasetpath+"/log.txt")
    res = True
    for file in files:
        if file != "log.txt" and not check_log_update_after_file_modified(datasetpath+"/"+file, logtime):
            res = False
    return res

def check_log_update_after_file_modified(filepath, logtime):
    modified = os.path.getctime(filepath)
    return logtime >= modified
