import os
from src.file_ui.file_utils import remove_file_extension
from src.helper_functions_for_app import create_link_fo_fna

class GraphReader:
    """ Reads information from .graph-files
    """
    def __init__(self, directory):
        self.dir = directory

    def read_file(self, filename):
        """ Reads the files and returns the data for it

        Args:
            filename (str): file to read
        """
        name = remove_file_extension(filename, ".graph")

        with open(os.path.join(self.dir, filename), "r", encoding='utf-8') as file:
            line = file.readline()
            sources = []
            comments_for_conversion = []
            while line[0] == "#":
                comments_for_conversion.append(line)
                if "genomes" in line:
                    sources = self._get_sources(line)
                line = file.readline()
            data = file.readlines()
            edges = data
            no_of_edges = len(data)
            no_of_nodes = self._get_number_of_nodes(data)
            licence = None
            short_desc = None
        return (name, no_of_nodes, no_of_edges, sources, licence, comments_for_conversion, \
            edges, short_desc)

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
        list_of_names = source_names.split(" ")
        source_tuple_list = []
        for name in list_of_names:
            source_tuple_list.append((create_link_fo_fna(name), name))
        return source_tuple_list
