import re
import os
import gfapy
from src.file_ui.file_utils import remove_file_extension

class GfaToDimacsConverter:
    """ Converts .gfa format file to .dimacs
    """
    def __init__(self, directory):
        """ Sets the directory where the .gfa
        file is located

        Args:
            directory (str): path of the directory
        """
        self.dir = directory

    def convert_gfa_to_dimacs(self, gfa_filename):
        """ Makes a gfa-object from the gfa-file
        and extracts the information required for the
        dimacs file

        Args:
            gfa_filename (str): name for the file that needs reading
        """
        name = remove_file_extension(gfa_filename, ".gfa")
        name = name+".dimacs"
        filepath = os.path.join(self.dir, gfa_filename)
        gfa_object = gfapy.Gfa.from_file(filepath)
        nro_edges, edge_line_list = self.process_edges(gfa_object)
        problem_line = "p edge "+str(len(gfa_object.segments))+" "+str(nro_edges)+"\n"
        self.write_dimacs_file(name,  problem_line, edge_line_list)

    def write_dimacs_file(self, name, problem_line, edge_line_list):
        """This function writes the DIMACS file.

        Args:
            name (string): name for the file
            problem_line (string): problem line
            edge_line_list (list): list of edge lines as strings
        """
        path = self.dir + "/dimacs/"
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(os.path.join(path, name), "w", encoding='utf-8') as file:
            file.write(problem_line)
            for item in edge_line_list:
                file.write(item)
    
    def process_edges(self, gfa_object):
        """ Counts the edges of the gfa-object and makes
        a string list of the edges in .dimacs format

        Args:
            gfa_object : the gfa-object in question

        Returns:
            int, list: number of edges, list of edge-strings in .dimacs form
        """
        edge_line_list = []
        edge_duplicate_check = []
        if gfa_object.version == 'gfa1':
            nro_edges = len(gfa_object._gfa1_links)
            for line in gfa_object._gfa1_links:
                line = str(line)
                if line[0] == "L":
                    new_line = line.lstrip("L")
                    splits = re.split(r"[+|-]", new_line)
                    edges = {splits[0].strip(), splits[1].strip()}
                    if edges not in edge_duplicate_check:
                        string_line = "e "+splits[0].strip()+" "+splits[1].strip()+"\n"
                        edge_duplicate_check.append(edges)
                        edge_line_list.append(string_line)
        elif gfa_object.version == 'gfa2':
            nro_edges = len(gfa_object._gfa2_edges)
            for line in gfa_object._gfa2_edges:
                line = str(line)
                if line[0] == "E":
                    new_line = line.lstrip("E")
                    new_line = new_line.lstrip("*")
                    splits = re.split(r"[+|-]", new_line)
                    string_line = "e "+splits[0].strip()+" "+splits[1].strip()+"\n"
                    edge_line_list.append(string_line)     
        return nro_edges, edge_line_list
