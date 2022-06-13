import gfapy
import os
from src.file_ui.file_utils import read_graph_description, check_description_file_exists, remove_file_extension

class GfaReader:
    """ Reads information from .gfa-files
    """
    def __init__(self, dir):
        """ Sets the directory to read

        Args:
            dir (str): directory of the files
        """
        self.dir = dir
        
    def read_file(self, filename):
        """ Makes a gfa-object from the file using
           gfapy-library and reads the data from the gfa-object
        
        Args:
        filename (str): filename of the file

        Returns:
            name, nodes, edges, sources: data of the gfa-file
        """

        name = remove_file_extension(filename, ".gfa")
        filepath = os.path.join(self.dir, filename)
        gfa_object = gfapy.Gfa.from_file(filepath)
        nodes = len(gfa_object.segments)
        licence = None
        sources = []
        if gfa_object.version == 'gfa1':
            edges = len(gfa_object._gfa1_links)
        elif gfa_object.version == 'gfa2':
            edges = len(gfa_object._gfa2_edges)
        if check_description_file_exists(self.dir, name):
            name, licence, sources = read_graph_description(self.dir, name)
        if name is None:
            name = remove_file_extension(filename, ".gfa")
        return name, nodes, edges, sources, licence

