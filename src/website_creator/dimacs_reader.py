import os
import json
from src.file_ui.file_utils import remove_file_extension, check_file_extension

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
        name, licence, sources = self.read_dimacs_description(name)
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
                p, format, number_of_nodes, number_of_edges = line.split()
                number_of_nodes = int(number_of_nodes)
                number_of_edges = int(number_of_edges)
            if line[0] == "e":
                # these are edges, no need to read atm
                continue
        return (number_of_nodes, number_of_edges)

    def read_dimacs_description(self, name):
        filename = name + "_description.json"
        filepath = self.dir +"/"+ filename
        name = None
        licence = None
        sources = []
        if os.stat(filepath).st_size > 0:
            with open(filepath, encoding='utf-8') as file:
                content = json.loads(file.read())
                name = content["name"]
                licence = content["licence"]
                sources = [(content["sources"], content["sources"])]
        return name, licence, sources

