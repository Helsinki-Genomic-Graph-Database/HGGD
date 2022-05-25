from os import getenv, environ, path
from flask import render_template, Flask, send_from_directory
from src.calculator import calculator_service
from src.file_ui.graph_reader import GraphReader
from src.dataset import Dataset
from src.zip_creator import zipcreator_service


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config['DATA_FOLDER']='data'

# Reads the datasets
DIR = "data"
graphreader_service = GraphReader(DIR)
graphreader_service.run()
graph_list = graphreader_service.get_graph_list()
dataset1 = Dataset(graph_list)

def get_app():
    return app

@app.route("/index", methods=["GET"])
def render_index():
    """ Renders the index page
    Returns:
        html page
    """
    dataset_names = ["Dataset1"] # placeholder list for all datasets
    return render_template("index.html", dataset_names=dataset_names)

@app.route("/datasets/<dataset>", methods=["GET"])
def render_dataset(dataset):
    """ Render the pages for dataset
    Args:
        dataset (string): dataset name
    Returns:
        html page
    """
    graphs_total, avg_nodes, avg_edges = calculator_service.calculate_statistics(dataset1)
    total_nodes, total_edges = calculator_service.get_no_nodes_and_edges(dataset1)
    graphs = dataset1.get_graphs()
    namelist = []
    directory = get_datapath()
    zipfile = zipcreator_service.create_zip(dataset, directory)
    for graph in graphs:
        namelist.append(graph.get_names())
    return render_template("dataset.html", total_graphs=graphs_total, average_nodes=avg_nodes, \
        average_edges=avg_edges, total_edges=total_edges, total_nodes=total_nodes, \
        namelist=namelist, dataset= dataset, zipfile=zipfile)

@app.route("/graphs/<name>", methods=["GET"])
def render_graph(name):
    """ Renders the pages for graphs
    Args:
        name (string): name for graph
    Returns:
        html page
    """
    graph = dataset1.find_graph(name)
    name = graph.get_names()
    nodes = graph.get_nodes()
    edges = graph.get_edges()
    return render_template("graph.html",name=name, nodes=nodes, edges=edges)

@app.route('/data/zip/<path:filename>', methods=['GET'])
def download(filename):
    """ Downloads a zipfile of the dataset

    Args:
        filename (string): name of the zipfile

    Returns:
        zipfile
    """
    directory = path.join(get_datapath(), 'zip')
    return send_from_directory(directory=directory, path='', filename=filename)

def get_datapath():
    """ Returns the path of the datafolder of the datasets

    Returns:
        string: datafolder path
    """
    goal_directory = path.join(app.root_path, '..', app.config['DATA_FOLDER'])
    return path.normpath(goal_directory)

if __name__ == "__main__":
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
