import gfapy
import os

class GfaReader:
    """ Reads information from .gfa-files
    """
    def __init__(self, dir):
        """ Makes a gfa-object from the file using
           gfapy-library

        Args:
            filename (str): filename of the file
            dir (str): directory of the file
        """
        self.dir = dir
        
    def read_file(self, filename):
        """ Reads the data from the gfa-object

        Returns:
            _type_: _description_
        """
        name = filename[:-4]
        filepath = os.path.join(self.dir, filename)
        gfa_object = gfapy.Gfa.from_file(filepath)
        nodes = len(gfa_object.segments)
        if gfa_object.version == 'gfa1':
            edges = len(gfa_object._gfa1_links)
        elif gfa_object.version == 'gfa2':
            edges = len(gfa_object._gfa2_edges)
        sources = [("https://www.testing.fi", "www.testing.fi")]
        return name, nodes, edges, sources
