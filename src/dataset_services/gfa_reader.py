import os
import gfapy
from src.file_ui.file_utils import remove_file_extension

class GfaReader:
    """ Reads information from .gfa-files
    """
    def __init__(self, directory):
        """ Sets the directory to read

        Args:
            dir (str): directory of the files
        """
        self.dir = directory

    def read_file(self, filename):
        """ Makes a gfa-object from the file using
           gfapy-library and reads the data from the gfa-object

        Args:
        filename (str): filename of the file

        Returns:
            name, nodes, edges, sources, licence: data of the gfa-file
        """

        name = remove_file_extension(filename, ".gfa")
        filepath = os.path.join(self.dir, filename)
        gfa_object = gfapy.Gfa.from_file(filepath)
        nodes = len(gfa_object.segments)
        licence = None
        sources = []
        short_desc = None
        if gfa_object.version == 'gfa1':
            edges = len(gfa_object._gfa1_links)
        elif gfa_object.version == 'gfa2':
            edges = len(gfa_object._gfa2_edges)
        return name, nodes, edges, sources, licence,None, None, short_desc
