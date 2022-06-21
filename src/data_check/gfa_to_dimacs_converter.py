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
        nro_nodes, nro_edges, edge_line_list = self.process_edges(gfa_object)
        problem_line = "p edge "+str(nro_nodes)+" "+str(nro_edges)+"\n"
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
        node_dict = {}
        new_node_name = 1
        if gfa_object.version == 'gfa1':
            for line in gfa_object._gfa1_links:
                line = str(line)
                if line[0] == "L":
                    new_line = line.lstrip("L")
                    new_line_parts = new_line.split() # should be 'node1' 'orientation1' 'node2' 'orientation2' ...
                    node1a_str = str(new_line_parts[0])+str(new_line_parts[1])
                    node1b_str = str(new_line_parts[0])+self.change_orientation(str(new_line_parts[1]))
                    node2a_str = str(new_line_parts[2])+str(new_line_parts[3])
                    node2b_str = str(new_line_parts[2])+self.change_orientation(str(new_line_parts[3]))
                    nodes = [node1a_str, node1b_str, node2a_str, node2b_str]
                    for node in nodes:
                        if not node in node_dict:
                            node_dict[node] = str(new_node_name)
                            new_node_name += 1
                    string_line = "e "+node_dict[node1a_str]+" "+node_dict[node2a_str]+"\n"
                    edge_line_list.append(string_line)
                    string_line = "e "+node_dict[node2b_str]+" "+node_dict[node1b_str]+"\n"
                    edge_line_list.append(string_line)
        elif gfa_object.version == 'gfa2':
            # THERE ARE NO TEST FOR THIS BECAUSE WE DIDN'T FIND SUITABLE FILES
            for line in gfa_object._gfa2_edges:
                line = str(line)
                if line[0] == "E":
                    # Edge line format should be "E <eid:opt_id> <sid1:ref> <sid2:ref> <beg1:pos> <end1:pos> <beg2:pos> <end2:pos> <alignment> <tag>*
                    # where the nodes are "<sid1:ref>" and "<sid2:ref>"
                    # e.g. "E * s1+ s2- b1 e1 b2 e2" -> nodes are "s1+" and "s2-"
                    new_line = line.lstrip("E")
                    new_line_parts = new_line.split()
                    node1a = new_line_parts[1]
                    orientation = node1a[-1]
                    other_orientation = self.change_orientation(orientation)
                    node1b = node1a[0:-1]+other_orientation
                    node2a = new_line_parts[2]
                    orientation = node2a[-1]
                    other_orientation = self.change_orientation(orientation)
                    node2b = node2a[0:-1]+other_orientation
                    nodes = [node1a, node1b, node2a, node2b]
                    for node in nodes:
                        if not node in node_dict:
                            node_dict[node] = str(new_node_name)
                            new_node_name += 1
                    string_line = "e "+node_dict[node1a]+" "+node_dict[node2a]+"\n"
                    edge_line_list.append(string_line)
                    string_line = "e "+node_dict[node2b]+" "+node_dict[node1b]+"\n"
                    edge_line_list.append(string_line)
        nro_edges = len(edge_line_list)
        nro_nodes = new_node_name-1
        return nro_nodes, nro_edges, edge_line_list

    def change_orientation(self, orientation):
        if orientation == "-":
            orientation = "+"
        elif orientation == "+":
            orientation = "-"
        return orientation