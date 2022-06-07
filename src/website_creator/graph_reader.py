"""Reads graph files from a directory"""
import os
from src.entities.graph import Graph
from src.file_ui.file_utils import check_file_extension
from src.file_ui.file_utils import list_licence_files, read_licence_files


class GraphReader:
    """reads graph files and makes graph objects and puts them to a list
    """
    def __init__(self, directory, dataset_licence, has_licence_file):
        """

        Args:
            dir (str): directory for the dataset
            dataset_licence (str): Licence for the dataset
            has_licence_file (bool): Dataset has different licences for some graphs
        """
        self.files = []
        self.graph_list = []
        self.dir = directory
        self.dataset_licence = dataset_licence
        self.has_licence_file = has_licence_file
        self.set_sources = set()

    def get_graph_list(self):
        """
        returns list of graph objects
        """
        return self.graph_list

    def get_set_sources(self):
        """ Returns the sources for the dataset

        Returns:
            set: sources for the dataset
        """
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
            new_graph = Graph(name, nodes, edges, sources, self.dataset_licence)
            self.graph_list.append(new_graph)
            if self.has_licence_file:
                self._add_licence(new_graph)

    def _read_file(self, filename):
        """ Reads the files and returns the data for it

        Args:
            filename (str): file to read

        Returns:
            int, str: number of nodes and edges, names of sources
        """
        with open(os.path.join(self.dir, filename), "r", encoding='utf-8') as file:
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
        """ Read the number of nodes from the file
        """
        nodes = set()

        for edge in data:
            edge = edge.split(" ")
            nodes.add(edge[0])
            nodes.add(edge[1])

        return len(nodes)

    def _get_sources(self, line):
        """ Reads the sources from the file
        """
        source_names = line.split(":")[1].strip()
        return source_names.split(" ")

    def _add_licence(self, new_graph):
        """ Adds a licence from the licence file from the graph

        Args:
            new_graph (graph)
        """
        licence_file_list = list_licence_files(self.dir)
        for licence_file in licence_file_list:
            licence_in_file = read_licence_files(self.dir, licence_file, new_graph)
            if licence_in_file:
                new_graph.set_licence(licence_file.strip(".licence"))
