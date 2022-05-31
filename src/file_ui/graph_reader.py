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
        self.set_sources = set()

    def get_graph_list(self):
        """
        returns list of graph objects
        """
        return self.graph_list

    def get_set_sources(self):
        return sorted(self.set_sources)

    def run(self):
        """scans the directory and creates the graph list
        """
        self.files = os.listdir(self.dir)
        for filename in self.files:
            if not check_file_extension(filename, "graph"):
                continue
            name = filename[:-6]
            nodes, edges, sources = self._read_file(filename)
            self.graph_list.append(Graph(name, nodes, edges, sources))

    def _read_file(self, filename):

        with open(os.path.join(self.dir, filename), "r") as file:
            line = file.readline()
            sources = []
            while line[0] == "#":
                if "genomes" in line:
                    sources = self._get_sources(line)
                    self.set_sources.update(sources)

                line = file.readline()
            data = file.readlines()
            edges = len(data)
            nodes = self._get_number_of_nodes(data)

        return (nodes, edges, sources)

    def _get_number_of_nodes(self, data):

        nodes = set()

        for edge in data:
            edge = edge.split(" ")
            nodes.add(edge[0])
            nodes.add(edge[1])

        return len(nodes)

    def _get_sources(self, line):
        source_names = line.split(":")[1].strip()
        return source_names.split(" ")
