from os import getenv, environ, path
from flask import render_template, Flask, send_from_directory
from src.dataset_services.dataset_creator import DatasetCreator
from src.dataset_services.dataset_reader import DatasetReader
from src.website_creator.read_graphs import ReadGraphs
from src.helper_functions_for_app import find_dataset_by_foldername, get_datapath


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config['DATA_FOLDER']='data'

# Finds dataset info from datafolder and makes a list of all the
# dataset objects with the info from the folders
DIR = "data"
datasetreader_service = DatasetReader(DIR)
dir_paths = datasetreader_service.get_paths()
datasetcreator_service = DatasetCreator(dir_paths)
dataset_list = datasetcreator_service.get_datasets()
graph_update_service = ReadGraphs(dataset_list)
graph_update_service.run()
dataset_list = graph_update_service.get_dataset_list_with_graphs()

def get_app():
    """ For tests
    """
    return app

@app.route("/hggd/index", methods=["GET"])
def render_index():
    """ Renders the index page
    Returns:
        html page
    """
    dataset_info = []
    for dataset in dataset_list:
        dataset_info.append((dataset.get_name(), dataset.get_descr_short(), \
        dataset.get_folder_name(), dataset.get_total_edges(), dataset.get_total_nodes()))
    return render_template("index.html", dataset_info=dataset_info)

@app.route("/hggd/datasets/<dataset>", methods=["GET"])
def render_dataset(dataset):
    """ Render the pages for dataset
    Args:
        dataset (string): dataset name
    Returns:
        html page
    """
    current_dataset = find_dataset_by_foldername(dataset, dataset_list)
    graphs_total, avg_nodes, avg_edges, total_nodes, total_edges = current_dataset.get_statistics()
    zipfile = current_dataset.get_zipfile_path()
    dataset_name = current_dataset.get_name()
    long_description = current_dataset.get_descr_long_for_dataset_html()
    licence = current_dataset.get_licence()
    user_defined_columns = current_dataset.get_user_defined_columns()
    graph_namelist = []
    graphs = current_dataset.get_list_of_graphs()
    sources = current_dataset.get_dataset_source()
    over_ten_sources = False
    nro_of_sources = len(sources)
    if nro_of_sources > 10:
        over_ten_sources = True
    for graph in graphs:
        graph_namelist.append(graph.get_names())
    return render_template("dataset.html", total_graphs=graphs_total, average_nodes=avg_nodes, \
        average_edges=avg_edges, total_edges=total_edges, total_nodes=total_nodes, \
        dataset_name = dataset_name, graph_namelist=graph_namelist, dataset= dataset, \
        zipfile=zipfile, long_description = long_description, licence=licence, \
        source_tuples = sources, user_defined_columns = user_defined_columns, \
        over_ten_sources=over_ten_sources, nro_of_sources=nro_of_sources)

@app.route("/hggd/datasets/<dataset>/<name>", methods=["GET"])
def render_graph(dataset, name):
    """ Renders the pages for graphs
    Args:
        dataset (string): name of dataset where the graph is included
        name (string): name for graph
    Returns:
        html page
    """
    current_dataset = find_dataset_by_foldername(dataset, dataset_list)
    graph = current_dataset.find_graph(name)
    name = graph.get_names()
    licence = graph.get_licence()
    nodes = graph.get_nodes()
    edges = graph.get_edges()
    sources = graph.get_sources()
    over_ten_sources = False
    nro_of_sources = len(sources)
    if nro_of_sources > 10:
        over_ten_sources = True
    dataset_folder = current_dataset.get_folder_name()
    return render_template("graph.html",name=name, nodes=nodes, edges=edges, dataset=dataset_folder, \
        licence=licence, source_tuples=sources, over_ten_sources=over_ten_sources, \
        nro_of_sources=nro_of_sources)

@app.route("/hggd/datasets/<dataset>/sources", methods=["GET"])
def render_dataset_sources(dataset):
    """ Renders the link page to source files for a dataset

    Args:
        dataset (string): name of dataset

    Returns:
        html page
    """
    current_dataset = find_dataset_by_foldername(dataset, dataset_list)
    dataset_name = current_dataset.get_name()
    sources = current_dataset.get_dataset_source()
    dataset_folder = current_dataset.get_folder_name()
    return render_template("genomelinks.html", name=dataset_name, \
    dataset=dataset_folder, source_tuples=sources)

@app.route("/hggd/datasets/<dataset>/<name>/sources", methods=["GET"])
def render_graph_sources(dataset, name):
    """ Renders the link page to source files for a graph

    Args:
        dataset (string): name of dataset where the graph is included
        name (string): name of the graph

    Returns:
        html page
    """
    current_dataset = find_dataset_by_foldername(dataset, dataset_list)
    graph = current_dataset.find_graph(name)
    graph_name = graph.get_names()
    sources = graph.get_sources()
    dataset_folder = current_dataset.get_folder_name()
    return render_template("genomelinks.html", name=graph_name, \
    dataset=dataset_folder, source_tuples=sources, graph=graph_name)

@app.route('/hggd/data/<dataset>/zip/<path:filename>', methods=['GET'])
def download_zip(dataset, filename):
    """ Downloads a zipfile of the dataset

    Args:
        dataset (string): name of dataset
        filename (string): name of the zipfile

    Returns:
        zipfile
    """
    directory = path.join(get_datapath(dataset, app), 'zip')
    return send_from_directory(directory=directory, path='', filename=filename)

@app.route('/hggd/data/<dataset>/<path:name>', methods=['GET'])
def download_graph(dataset, name):
    """ Downloads a specific graph file

    Args:
        dataset (str): dataset folder of the graph
        name (str): name of the graph

    Returns:
        .graph file
    """
    current_dataset = find_dataset_by_foldername(dataset, dataset_list)
    graph = current_dataset.find_graph(name)
    graph_filename = graph.get_file_name()
    directory=get_datapath(dataset, app)
    return send_from_directory(directory=directory, path='', filename=graph_filename)


if __name__ == "__main__":
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
