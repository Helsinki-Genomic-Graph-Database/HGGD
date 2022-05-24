"""Reads graph files from a directory"""
import os
from src.graph import Graph

DIR = "src/tests/testdata"

class GraphReader:
    """reads graph files and makes graph objects and puts them to a list
    """
    def __init__(self):
        self.files = []
        self.graph_list = []

    def get_graph_list(self):
        """
        returns list of graph objects
        """
        return self.graph_list

    def run(self):
        """scans the directory and creates the graph list
        """
        self.files = os.listdir(DIR)
        for filename in self.files:
            name = filename[:-6]
            nodes, edges = self._read_file(filename)
            self.graph_list.append(Graph(name, nodes, edges))

    def _read_file(self, filename):

        nodes = None
        edges = None

        with open(os.path.join(DIR, filename), "r") as file:
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

graphreader_service = GraphReader()
