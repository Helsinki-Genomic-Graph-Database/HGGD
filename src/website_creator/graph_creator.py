"""Reads graph files from a directory"""
import os
from src.entities.graph import Graph
from src.file_ui.file_utils import check_file_extension, check_file_extension_multiple, read_graph_description, check_description_file_exists, create_source_txt_file
from src.website_creator.graph_reader import GraphReader
from src.website_creator.gfa_reader import GfaReader
from src.website_creator.dimacs_reader import DimacsReader

class GraphCreator:
    """reads graph files and makes graph objects and puts them to a list
    """
    def __init__(self, directory, dataset_licence, graph_info = []):
        """

        Args:
            dir (str): directory for the dataset
            dataset_licence (str): Licence for the dataset
            graph_info (list): list of tuples, format: (graph filename, licence, \
                has sources (bool), has_short_desc(bool), desc_file_exists(bool))
        """
        self.files = []
        self.graph_list = []
        self.dir = directory
        self.dataset_licence = dataset_licence
        self.graph_info = graph_info
        self.set_sources = set()
        self.set_licences = set()
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

    def get_set_licences(self):
        return sorted(self.set_licences)

    def run(self):
        """scans the directory and creates the graph list
        """
        self.files = os.listdir(self.dir)
        for filename in self.files:
            if os.path.isdir(os.path.join(self.dir, filename)):
                continue
            if not check_file_extension_multiple(filename, self.formats):
                continue

            name = None
            licence = None
            sources = []
            short_desc = None
            user_defined_columns = None

            if len(self.dataset_licence) > 0:
                licence = self.dataset_licence[0]
            else:
                licence = None
            if check_file_extension(filename, "graph"):
                graphreader = GraphReader(self.dir)
                name, nodes, edges, sources, licence, comments_for_conversion, edges_listed, \
                    short_desc = graphreader.read_file(filename)
                fileformat = "graph"
            if check_file_extension(filename, "gfa"):
                graphreader = GfaReader(self.dir)
                name, nodes, edges, sources, licence, short_desc = graphreader.read_file(filename)
                fileformat = "gfa"
            if check_file_extension(filename, "dimacs"):
                dimacsreader = DimacsReader(self.dir)
                name, nodes, edges, sources, licence, short_desc \
                    = dimacsreader.read_dimacs_graph(filename)
                fileformat = "dimacs"
            for graph in self.graph_info:
                if graph[0] == filename:
                    licence = graph[1]

            

            extension_length = len(filename.split(".")[-1])+1
            filename_without_extension = filename[:-extension_length]

            if check_description_file_exists(self.dir, filename_without_extension):
                
                name, licence, sources_desc, short_desc, user_defined_columns = read_graph_description(self.dir, filename_without_extension)
                if len(sources_desc) > 0:
                    sources = sources_desc

            if name is None:
                name = filename_without_extension

            if licence is None:
                if len(self.dataset_licence) > 0:
                    licence = self.dataset_licence[0]
            new_graph = Graph(name, nodes, edges, sources, licence, filename, fileformat, \
                short_desc, user_defined_columns)

            if len(sources) > 0:
                create_source_txt_file(self.dir, filename_without_extension, sources)
            self.set_sources.update(sources)
            if licence is not None:
                self.set_licences.update([licence])
            self.graph_list.append(new_graph)
