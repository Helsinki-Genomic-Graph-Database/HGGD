from os import getenv, environ
from flask import render_template, Flask
from calculator import calculator_service
from file_ui.graphReader import graphreader_service
from dataset import Dataset



app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")


# Reads the datasets
graphreader_service.run()
graph_list = graphreader_service.get_graph_list()
dataset1 = Dataset(graph_list)

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
    for graph in graphs:
        namelist.append(graph.get_names())
    return render_template("dataset.html", total_graphs=graphs_total, average_nodes=avg_nodes, \
        average_edges=avg_edges, graphs=graphs, total_edges=total_edges, \
        total_nodes=total_nodes, namelist=namelist, dataset= dataset)

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

if __name__ == "__main__":
    port = int(environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)