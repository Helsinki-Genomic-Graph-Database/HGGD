import os
import gfapy
from src.file_ui.file_utils import remove_file_extension

class GfaToDimacsConverter:
    """ Converts .gfa format file to .dimacs format, which includes:
    comment lines starting with 'c', problem lines 'p edge {nodes} {edges}',
    and edge lines 'e {node1} {node2}'.
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
        nro_nodes = self.calculate_nodes(gfa_object)
        nro_edges, edge_line_list = self.process_edges(gfa_object)
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

    def calculate_nodes(self, gfa_object):
        nodes = 0
        for line in gfa_object.lines:
            line = str(line)
            if line[0] == "S":
                nodes += 1
        return nodes

    def process_edges(self, gfa_object):
        """Calls for the edge processing functions based on gfa format.

        Args:
            gfa_object : the gfa-object in question

        Returns:
            int, list: number of edges, list of edge-strings in .dimacs form
        """
        if gfa_object.version == 'gfa1':
            nro_edges, edge_line_list = self.process_gfa1_edges(gfa_object)
        elif gfa_object.version == 'gfa2':
            nro_edges, edge_line_list = self.process_gfa2_edges(gfa_object)
        return nro_edges, edge_line_list

    def process_gfa1_edges(self, gfa_object):
        """Counts the edges of the gfa-object and makes
        a string list of the edges in .dimacs format

        Args:
            gfa_object : the gfa-object in question in gfa 1 form

        Returns:
            int, list: number of edges, list of edge-strings in .dimacs form
        """
        edge_line_list = []
        gfa_nodes = set()
        for line in gfa_object._gfa1_links:
            line = str(line)
            if line[0] == "L":
                node1a_str, node1b_str, node2a_str, node2b_str = self.process_edge_lines_gfa1(line)
                gfa_nodes.update([node1a_str, node1b_str, node2a_str, node2b_str])
        node_dict = self.map_gfa_nodes_with_dimacs_nodes(gfa_nodes)
        # node_dict: key: gfa node, value: dimacs node
        for line in gfa_object._gfa1_links:
            line = str(line)
            if line[0] == "L":
                node1a_str, node1b_str, node2a_str, node2b_str = self.process_edge_lines_gfa1(line)
                original_line = "e "+node_dict[node1a_str]+" "+node_dict[node2a_str]+"\n"
                if not original_line in edge_line_list:
                    edge_line_list.append(original_line)
                opposite_if_original_line = "e "+node_dict[node2b_str]+" "+node_dict[node1b_str]+"\n"
                if not opposite_if_original_line in edge_line_list:
                    edge_line_list.append(opposite_if_original_line)
        nro_edges = len(edge_line_list)
        return nro_edges, edge_line_list

    def process_gfa2_edges(self, gfa_object):
        """ Counts the edges of the gfa-object and makes
        a string list of the edges in .dimacs format

        Args:
            gfa_object : the gfa-object in question in gfa 2 form

        Returns:
            int, list: number of edges, list of edge-strings in .dimacs form
        """
        edge_line_list = []
        # THERE ARE NO TESTS FOR THIS BECAUSE WE DIDN'T FIND SUITABLE FILES
        gfa_nodes = set()
        for line in gfa_object._gfa2_edges:
            line = str(line)
            if line[0] == "E":
                node1a, node1b, node2a, node2b = self.process_edge_lines_gfa2(line)
                gfa_nodes.update([node1a, node1b, node2a, node2b])
        # node_dict: key: gfa node, value: dimacs node
        node_dict = self.map_gfa_nodes_with_dimacs_nodes(gfa_nodes)
        for line in gfa_object._gfa2_edges:
            line = str(line)
            if line[0] == "E":
                node1a, node1b, node2a, node2b = self.process_edge_lines_gfa2(line)
                original_line = "e "+node_dict[node1a]+" "+node_dict[node2a]+"\n"
                if not original_line in edge_line_list:
                    edge_line_list.append(original_line)
                opposite_if_original_line = "e "+node_dict[node2b]+" "+node_dict[node1b]+"\n"
                if not opposite_if_original_line in edge_line_list:
                    edge_line_list.append(opposite_if_original_line)
        nro_edges = len(edge_line_list)
        return nro_edges, edge_line_list

    def map_gfa_nodes_with_dimacs_nodes(self, gfa_node_set):
        """Gives nodes new names for the DIMACS files.

        Args:
            gfa_node_set (set): nodes

        Returns:
            dict: nodes
        """
        gfa_node_list = sorted(gfa_node_set)
        new_node_name = 1
        node_dict = {}
        for node in gfa_node_list:
            if not node in node_dict:
                node_dict[node] = str(new_node_name)
                new_node_name += 1
        return node_dict

    def change_orientation(self, orientation):
        """Changes the orientation of a node. Orientation can be '-' or '+'.

        Args:
            orientation (string): '-' or '+'.

        Returns:
            string: '-' or '+'.
        """
        if orientation == "-":
            orientation = "+"
        elif orientation == "+":
            orientation = "-"
        return orientation

    def process_edge_lines_gfa1(self, line):
        new_line = line.lstrip("L")
        new_line_parts = new_line.split() # form: 'node1' 'orientation1' 'node2' 'orientation2'...
        node1a_str = str(new_line_parts[0])+str(new_line_parts[1])
        node1b_str = str(new_line_parts[0])+self.change_orientation(str(new_line_parts[1]))
        node2a_str = str(new_line_parts[2])+str(new_line_parts[3])
        node2b_str = str(new_line_parts[2])+self.change_orientation(str(new_line_parts[3]))
        return node1a_str, node1b_str, node2a_str, node2b_str

    def process_edge_lines_gfa2(self, line):
        # Edge line format should be "E <eid:opt_id> <sid1:ref> <sid2:ref> ...
        # <beg1:pos> <end1:pos> <beg2:pos> <end2:pos> <alignment> <tag>*
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
        return node1a, node1b, node2a, node2b
