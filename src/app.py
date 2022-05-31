from os import getenv, environ, path
from flask import render_template, Flask, send_from_directory
from src.calculator import calculator_service
from src.file_ui.graph_reader import GraphReader
from src.file_ui.dataset_reader import DatasetReader
from src.dataset import Dataset
from src.zip_creator import zipcreator_service
from src.file_ui.file_utils import read_description


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config['DATA_FOLDER']='data'

# Finds dataset info from datafolder and makes a list of all the
# dataset objects with the info from the folders
DIR = "data"
datasetreader_service = DatasetReader(DIR)
dir_paths = datasetreader_service.get_paths()
dataset_list = []
for datasetpath in dir_paths:
    graphreader_service = GraphReader(datasetpath)
    graphreader_service.run()
    graph_list = graphreader_service.get_graph_list()
    name, descr_short, descr_long, licence = read_description(datasetpath)
    dataset_list.append(Dataset(name, graph_list, descr_short, descr_long, licence, datasetpath))



def get_app():
    """ For tests
    """
    return app




@app.route("/index", methods=["GET"])
def render_index():
    """ Renders the index page
    Returns:
        html page
    """
    dataset_names = []
    for dataset in dataset_list:
        dataset_names.append((dataset.get_name(), dataset.get_descr_short(), \
        dataset.get_foldername()))
    return render_template("index.html", dataset_names=dataset_names)

@app.route("/datasets/<dataset>", methods=["GET"])
def render_dataset(dataset):
    """ Render the pages for dataset
    Args:
        dataset (string): dataset name
    Returns:
        html page
    """
    current_dataset = find_dataset_by_foldername(dataset)
    graphs_total, avg_nodes, avg_edges = calculator_service.calculate_statistics(current_dataset)
    total_nodes, total_edges = calculator_service.get_no_nodes_and_edges(current_dataset)
    directory = get_datapath(current_dataset.get_foldername())
    zipfile = zipcreator_service.create_zip(dataset, directory)
    dataset_name = current_dataset.get_name()
    long_description = current_dataset.get_descr_long()
    licence = current_dataset.get_licence()
    graph_namelist = []
    graphs = current_dataset.get_graphs()
    for graph in graphs:
        graph_namelist.append(graph.get_names())
    return render_template("dataset.html", total_graphs=graphs_total, average_nodes=avg_nodes, \
        average_edges=avg_edges, total_edges=total_edges, total_nodes=total_nodes, \
        dataset_name = dataset_name, graph_namelist=graph_namelist, dataset= dataset, \
        zipfile=zipfile, long_description = long_description, licence=licence)

@app.route("/datasets/<dataset>/<name>", methods=["GET"])
def render_graph(dataset, name):
    """ Renders the pages for graphs
    Args:
        name (string): name for graph
    Returns:
        html page
    """
    current_dataset = find_dataset_by_foldername(dataset)
    graph = current_dataset.find_graph(name)
    name = graph.get_names()
    licence = current_dataset.get_licence()
    nodes = graph.get_nodes()
    edges = graph.get_edges()
    dataset_folder = current_dataset.get_foldername()
    return render_template("graph.html",name=name, nodes=nodes, edges=edges, \
    dataset=dataset_folder, licence=licence)

@app.route('/data/<dataset>/zip/<path:filename>', methods=['GET'])
def download_zip(dataset, filename):
    """ Downloads a zipfile of the dataset

    Args:
        filename (string): name of the zipfile

    Returns:
        zipfile
    """
    directory = path.join(get_datapath(dataset), 'zip')
    return send_from_directory(directory=directory, path='', filename=filename)

@app.route('/data/<dataset>/<path:name>', methods=['GET'])
def download_graph(dataset, name):
    """ Downloads a specific graph file

    Args:
        dataset (str): dataset folder of the graph
        name (str): name of the graph

    Returns:
        .graph file
    """
    directory=get_datapath(dataset)
    graphfilename = ".".join([name, "graph"])
    return send_from_directory(directory=directory, path='', filename=graphfilename)

def get_datapath(dataset_name):
    """ Returns the path of the datafolder of the datasets

    Returns:
        string: datafolder path
    """
    goal_directory = path.join(app.root_path, '..', app.config['DATA_FOLDER'], dataset_name)
    return path.normpath(goal_directory)

def find_dataset_by_foldername(dataset_name):
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

if __name__ == "__main__":
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
