from os import path

def find_dataset_by_foldername(dataset_name, dataset_list):
    """ Finds dataset by foldername

    Args:
        dataset_name (srt): name of the dataset folder

    Returns:
        dataset-object
    """
    for dataset in dataset_list:
        if dataset.get_folder_name() == dataset_name:
            return dataset
    return None

def get_datapath(dataset_name, app):
    """ Returns the path of the datafolder of the datasets

    Returns:
        string: datafolder path
    """
    goal_directory = path.join(app.root_path, '..', app.config['DATA_FOLDER'], dataset_name)
    return path.normpath(goal_directory)

def create_link_fo_fna(text):

    link = "https://ftp.ncbi.nlm.nih.gov/genomes/all/"

    text_list = text.strip().split("_")

    link = link+text_list[0]+"/"

    numbers = text_list[1]

    link = link+numbers[:3]+"/"
    numbers = numbers[3:]
    link = link+numbers[:3]+"/"
    numbers = numbers[3:]
    link = link+numbers[:3]+"/"
    link = link+text[:-4]+"/"+text[:-4]+"_genomic.fna.gz"

    return link