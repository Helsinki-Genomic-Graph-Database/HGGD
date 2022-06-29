import os
from src.file_ui.file_utils import remove_file_extension, read_graph_description, check_description_file_exists

class GraphReader:
    """ Reads information from .graph-files
    """
    def __init__(self, directory):
        self.dir = directory

    def read_file(self, filename):
        """ Reads the files and returns the data for it

        Args:
            filename (str): file to read

        Returns:
            int, str: number of nodes and edges, names of sources
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
        # if check_description_file_exists(self.dir, name):
        #     name, licence, sources_desc, short_desc = read_graph_description(self.dir, name)
        #     if len(sources_desc) > 0:
        #         sources = sources_desc
        # if name is None:
        #     name = remove_file_extension(filename, ".graph")
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
            source_tuple_list.append((self.create_link_fo_fna(name), name))
        return source_tuple_list

    def create_link_fo_fna(self, text):

        link = "https://ftp.ncbi.nlm.nih.gov/genomes/all/"

        text_list = text.strip().split("_")

        link = link+text_list[0]+"/"

        numbers = text_list[1]

        link = link+numbers[:3]+"/"
        numbers = numbers[3:]
        link = link+numbers[:3]+"/"
        numbers = numbers[3:]
        link = link+numbers[:3]+"/"
        link = link+text[:-4]+"/"+text[:-4]+"_genomic.fna.gz"

        return link
