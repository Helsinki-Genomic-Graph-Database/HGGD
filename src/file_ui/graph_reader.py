"""Reads graph files from a directory"""
import os
from src.graph import Graph
from src.file_ui.file_utils import check_file_extension



class GraphReader:
    """reads graph files and makes graph objects and puts them to a list
    """
    def __init__(self, dir):
        self.files = []
        self.graph_list = []
        self.dir = dir

    def get_graph_list(self):
        """
        returns list of graph objects
        """
        return self.graph_list

    def run(self):
        """scans the directory and creates the graph list
        """
        self.files = os.listdir(self.dir)
        for filename in self.files:
            if not check_file_extension(filename, "graph"):
                continue
            name = filename[:-6]
            nodes, edges = self._read_file(filename)
            self.graph_list.append(Graph(name, nodes, edges))

    def _read_file(self, filename):

        with open(os.path.join(self.dir, filename), "r") as file:
            line = file.readline()
            while line[0] == "#":
                line = file.readline()
            data = file.readlines()
            edges = len(data)
            nodes = self._get_number_of_nodes(data)

        return (nodes, edges)

    def _get_number_of_nodes(self, data):

        nodes = set()

        for edge in data:
            edge = edge.split(" ")
            nodes.add(edge[0])
            nodes.add(edge[1])

        return len(nodes)
