from flask import render_template
from calculator import calculator_service
from dataset import Dataset
from app import app
from graph import Graph

graph_list = [Graph("name1", 11, 12), Graph("name2", 13, 14), Graph("name3", 15, 16)]
dataset1 = Dataset(graph_list)

@app.route("/", methods=["GET"])
def render_index():
    return render_template("index.html")

@app.route("/dataset", methods=["GET"])
def render_dataset():
    graphs_total, avg_nodes, avg_edges = calculator_service.calculate_statistics(dataset1)
    total_nodes, total_edges = calculator_service.get_no_nodes_and_edges(dataset1)
    graphs = dataset1.get_graphs()
    namelist = []
    for graph in graphs:
        namelist.append(graph.get_names())
    return render_template("dataset.html", total_graphs=graphs_total, average_nodes=avg_nodes, \
        average_edges=avg_edges, graphs= graphs, total_edges=total_edges, \
        total_nodes= total_nodes, namelist=namelist)

@app.route("/<name>", methods=["GET"])
def render_graph(name):
    graph = dataset1.find_graph(name)
    name = graph.get_names()
    nodes = graph.get_nodes()
    edges = graph.get_edges()
    return render_template("graph.html",name = name, nodes = nodes, edges = edges)
