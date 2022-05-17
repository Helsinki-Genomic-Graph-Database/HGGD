import os
from graph import Graph

DIR = "tests/testdata"

class GraphReader:

    def __init__(self):
        self.files = []
        self.graph_list = []

    def get_graph_list(self):
        return self.graph_list

    def run(self):
        self.files = os.listdir(DIR)
        for filename in self.files:
            name = filename[:-6]
            nodes_and_edges = self._read_file(filename)
            nodes = nodes_and_edges[0]
            edges = nodes_and_edges[1]
            self.graph_list.append(Graph(name, nodes, edges))

    def _read_file(self, filename):

        nodes = None
        edges = None

        with open(os.path.join(DIR, filename), "r") as file:
            file.readline()
            file.readline()
            file.readline()
            nodes = self._get_number_of_nodes(file.readline())
            edges = int(file.readline())

        return (nodes, edges)

    def _get_number_of_nodes(self, line):
        line = line.strip()
        split_line = line.split(" ")
        return len(split_line) - 2