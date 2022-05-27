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

# Reads the datasets and makes a list of all of them
DIR = "data"
datasetreader_service = DatasetReader(DIR)
dir_paths = datasetreader_service.get_paths()
dataset_list = []
for datasetpath in dir_paths:
    graphreader_service = GraphReader(datasetpath)
    graphreader_service.run()
    graph_list = graphreader_service.get_graph_list()
    #name = datasetpath.strip().split("/")[-1]
    name, descr_short, descr_long = read_description(datasetpath)
    dataset_list.append(Dataset(name, graph_list, descr_short, descr_long))



def get_app():
    return app




@app.route("/index", methods=["GET"])
def render_index():
    """ Renders the index page
    Returns:
        html page
    """
    dataset_names = []
    for dataset in dataset_list:
        dataset_names.append(dataset.get_name())
    return render_template("index.html", dataset_names=dataset_names)

@app.route("/datasets/<dataset>", methods=["GET"])
def render_dataset(dataset):
    """ Render the pages for dataset
    Args:
        dataset (string): dataset name
    Returns:
        html page
    """
    current_dataset = find_dataset_by_name(dataset)
    graphs_total, avg_nodes, avg_edges = calculator_service.calculate_statistics(current_dataset)
    total_nodes, total_edges = calculator_service.get_no_nodes_and_edges(current_dataset)
    graphs = current_dataset.get_graphs()
    namelist = []
    directory = get_datapath(current_dataset.get_name())
    zipfile = zipcreator_service.create_zip(dataset, directory)
    for graph in graphs:
        namelist.append(graph.get_names())
    return render_template("dataset.html", total_graphs=graphs_total, average_nodes=avg_nodes, \
        average_edges=avg_edges, total_edges=total_edges, total_nodes=total_nodes, \
        namelist=namelist, dataset= dataset, zipfile=zipfile)

@app.route("/datasets/<dataset>/<name>", methods=["GET"])
def render_graph(dataset, name):
    """ Renders the pages for graphs
    Args:
        name (string): name for graph
    Returns:
        html page
    """
    current_dataset = find_dataset_by_name(dataset)
    graph = current_dataset.find_graph(name)
    graph_name = graph.get_names()
    nodes = graph.get_nodes()
    edges = graph.get_edges()
    return render_template("graph.html",name=graph_name, nodes=nodes, edges=edges)

@app.route('/data/<dataset>/zip/<path:filename>', methods=['GET'])
def download(dataset, filename):
    """ Downloads a zipfile of the dataset

    Args:
        filename (string): name of the zipfile

    Returns:
        zipfile
    """
    directory = path.join(get_datapath(dataset), 'zip')
    return send_from_directory(directory=directory, path='', filename=filename)

def get_datapath(dataset_name):
    """ Returns the path of the datafolder of the datasets

    Returns:
        string: datafolder path
    """
    goal_directory = path.join(app.root_path, '..', app.config['DATA_FOLDER'], dataset_name)
    return path.normpath(goal_directory)

def find_dataset_by_name(dataset_name):
    """ Finds dataset by name

    Args:
        dataset_name (str): dataset name

    Returns:
        dataset-object
    """
    for dataset in dataset_list:
        if dataset.get_name() == dataset_name:
            return dataset

if __name__ == "__main__":
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

