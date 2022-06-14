"""Reads graph files from a directory"""
import os
from src.entities.graph import Graph
from src.file_ui.file_utils import check_file_extension, check_file_extension_multiple
from src.file_ui.file_utils import list_licence_files, read_licence_files
from src.website_creator.graph_reader import GraphReader
from src.website_creator.gfa_reader import GfaReader
from src.website_creator.dimacs_reader import DimacsReader

class GraphCreator:
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
        self.formats = ["graph", "gfa", "dimacs"]

    def get_graph_list(self):
        """
        returns list of graph objects
        """
        return sorted(self.graph_list)

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
            if not check_file_extension_multiple(filename, self.formats):
                continue
            if len(self.dataset_licence) > 0:
                licence = self.dataset_licence[0]
            else:
                licence = None
            if check_file_extension(filename, "graph"):
                graphreader = GraphReader(self.dir)
                name, nodes, edges, sources, licence, comments_for_conversion, edges_listed = graphreader.read_file(filename)
                fileformat = "graph"
            if check_file_extension(filename, "gfa"):
                graphreader = GfaReader(self.dir)
                name, nodes, edges, sources, licence = graphreader.read_file(filename)
                fileformat = "gfa"
            if check_file_extension(filename, "dimacs"):
                dimacsreader = DimacsReader(self.dir)
                name, nodes, edges, sources, licence = dimacsreader.read_dimacs_graph(filename)
                fileformat = "dimacs"
            if licence is None:
                licence = self.dataset_licence[0]
            new_graph = Graph(name, nodes, edges, sources, licence, filename, fileformat)
            self.set_sources.update(sources)
            self.graph_list.append(new_graph)
            if self.has_licence_file:
                self._add_licence(new_graph)


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
