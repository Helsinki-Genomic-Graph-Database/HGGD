import os

class GraphReader:
    """ Reads information from .graph-files
    """
    def __init__(self, dir):
        self.dir = dir

    def read_file(self, filename):
        """ Reads the files and returns the data for it

        Args:
            filename (str): file to read

        Returns:
            int, str: number of nodes and edges, names of sources
        """
        
        name = filename[:-6]
        with open(os.path.join(self.dir, filename), "r", encoding='utf-8') as file:
            line = file.readline()
            sources = []
            while line[0] == "#":
                if "genomes" in line:
                    sources = self._get_sources(line)
                line = file.readline()
            data = file.readlines()
            edges = len(data)
            nodes = self._get_number_of_nodes(data)

        return (name, nodes, edges, sources)

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
        