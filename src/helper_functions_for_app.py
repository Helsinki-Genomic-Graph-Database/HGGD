from os import path

def find_dataset_by_foldername(dataset_name, dataset_list):
    """ Finds dataset by foldername

    Args:
        dataset_name (srt): name of the dataset folder

    Returns:
        dataset-object
    """
    for dataset in dataset_list:
        if dataset.get_foldername() == dataset_name:
            return dataset
    return None

def get_datapath(dataset_name, app):
    """ Returns the path of the datafolder of the datasets

    Returns:
        string: datafolder path
    """
    goal_directory = path.join(app.root_path, '..', app.config['DATA_FOLDER'], dataset_name)
    return path.normpath(goal_directory)