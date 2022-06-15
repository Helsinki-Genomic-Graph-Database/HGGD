import os
from src.file_ui.file_utils import remove_file_extension, read_graph_description, check_description_file_exists

class DimacsReader:
    """This class reads graph files in DIMACS format."""
    def __init__(self, directory):
        self.dir = directory

    def read_dimacs_graph(self, filename):
        """This function returns all the information about
        the dimacs graph, including the .dimacs-file as well
        as the description.json

        Args:
            filename (_type_): name of the .dimacs file
        """
        name = remove_file_extension(filename, ".dimacs")
        licence = None
        sources = []
        if check_description_file_exists(self.dir, name):
            name, licence, sources = read_graph_description(self.dir, name)
        number_of_nodes, number_of_edges = self.read_dimacs_file(filename)
        return name, number_of_nodes, number_of_edges, sources, licence

    def read_dimacs_file(self, filename):
        """ This function reads the .dimacs file and
        returns the total numbers of edges and nodes.

        Args:
            filename (str): file to read

        Returns:
            int, int: number of nodes, number of edges
        """
        lines = []
        with open(os.path.join(self.dir, filename), "r", encoding='utf-8') as file:
            lines = file.readlines()
        number_of_nodes = 0
        number_of_edges = 0
        for line in lines:
            if line[0] == "c":
                # skip comment line
                continue
            if line[0] == "p":
                # recognise number of nodes and edges
                # line format is: p FORMAT NODES EDGES
                letter_p, edge_format, number_of_nodes, number_of_edges = line.split()
                number_of_nodes = int(number_of_nodes)
                number_of_edges = int(number_of_edges)
            if line[0] == "e":
                # these are edges, no need to read atm
                continue
        return (number_of_nodes, number_of_edges)
