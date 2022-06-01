from os import getenv, environ, path
from flask import render_template, Flask, send_from_directory
from src.calculator import calculator_service
from src.file_ui.dataset_reader import DatasetReader
from src.zip_creator import zipcreator_service
from src.file_ui.file_utils import read_licence_names_from_files, read_licence_files, list_licence_files
from src.helper_functions_for_app import find_dataset_by_foldername, get_datapath, create_dataset, create_link_fo_fna


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
    dataset_list.append(create_dataset(datasetpath))


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
    current_dataset = find_dataset_by_foldername(dataset, dataset_list)
    graphs_total, avg_nodes, avg_edges = calculator_service.calculate_statistics(current_dataset)
    total_nodes, total_edges = calculator_service.get_no_nodes_and_edges(current_dataset)
    directory = get_datapath(current_dataset.get_foldername(), app)
    zipfile = zipcreator_service.create_zip(dataset, directory)
    dataset_name = current_dataset.get_name()
    long_description = current_dataset.get_descr_long()
    has_licence_files = current_dataset.get_has_licence_files()
    licence = current_dataset.get_licence()
    if has_licence_files:
        path = current_dataset.get_datasetpath()
        licence_from_files = read_licence_names_from_files(path)
        licence = licence + ", " + licence_from_files
    graph_namelist = []
    graphs = current_dataset.get_graphs()
    sources = current_dataset.get_sources()
    source_tuples = []
    for source in sources:
        source_tuples.append((create_link_fo_fna(source), source))
    for graph in graphs:
        graph_namelist.append(graph.get_names())
    return render_template("dataset.html", total_graphs=graphs_total, average_nodes=avg_nodes, \
        average_edges=avg_edges, total_edges=total_edges, total_nodes=total_nodes, \
        dataset_name = dataset_name, graph_namelist=graph_namelist, dataset= dataset, \
        zipfile=zipfile, long_description = long_description, licence=licence, source_tuples = source_tuples)

@app.route("/datasets/<dataset>/<name>", methods=["GET"])
def render_graph(dataset, name):
    """ Renders the pages for graphs
    Args:
        name (string): name for graph
    Returns:
        html page
    """
    current_dataset = find_dataset_by_foldername(dataset, dataset_list)
    graph = current_dataset.find_graph(name)
    name = graph.get_names()
    licence = current_dataset.get_licence()
    has_licence_files = current_dataset.get_has_licence_files()
    if has_licence_files:
        path = current_dataset.get_datasetpath()
        licence_file_list = list_licence_files(path)
        for licence_file in licence_file_list:
            licence_in_file = read_licence_files(path, licence_file, graph)
            if licence_in_file:
                licence = licence_file.strip(".licence")
    nodes = graph.get_nodes()
    edges = graph.get_edges()
    sources = graph.get_sources()
    source_tuples = []
    for source in sources:
        source_tuples.append((create_link_fo_fna(source), source))
    dataset_folder = current_dataset.get_foldername()
    return render_template("graph.html",name=name, nodes=nodes, edges=edges, \
    dataset=dataset_folder, licence=licence, source_tuples=source_tuples)

@app.route('/data/<dataset>/zip/<path:filename>', methods=['GET'])
def download_zip(dataset, filename):
    """ Downloads a zipfile of the dataset

    Args:
        filename (string): name of the zipfile

    Returns:
        zipfile
    """
    directory = path.join(get_datapath(dataset, app), 'zip')
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
    directory=get_datapath(dataset, app)
    graphfilename = ".".join([name, "graph"])
    return send_from_directory(directory=directory, path='', filename=graphfilename)


if __name__ == "__main__":
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
