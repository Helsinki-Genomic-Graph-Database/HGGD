import os
from src.website_creator.graph_reader import GraphReader

class GraphToDimacsConverter:
    """This class contains functions for converting a graph
    into DIMACS format, which includes: comment lines starting
    with 'c', problem lines 'p edge {nodes} {edges}', and edge lines
    'e {node1} {node2}'.
    """
    def __init__(self, directory):
        self.dir = directory
        self.graph_reader = GraphReader(self.dir)

    def convert_graph_to_dimacs(self, graph_filename):
        """This function reads graph, processes content and creates
        DIMACS file.

        Args:
            graph_filename (str): name for the file that needs reading
        """
        name, no_of_nodes, no_of_edges, comments_for_conversion, \
            edges = self._read_from_graph(graph_filename)
        name = name+".dimacs"
        processed_edges, edge_string = self._process_edges(edges)
        comments = self._process_comments(comments_for_conversion, edge_string)
        problem_line = "p edge "+str(no_of_nodes)+" "+str(no_of_edges)+"\n"
        edge_line_list = self._create_edge_line_list(processed_edges)
        self.write_dimacs_file(name, comments, problem_line, edge_line_list)

    def write_dimacs_file(self, name, comments, problem_line, edge_line_list):
        """This function writes the DIMACS file.

        Args:
            name (string): name for the file
            comments (list): list of comment lines as strings
            problem_line (string): problem line
            edge_line_list (list): list of edge lines as strings
        """
        path = self.dir + "/dimacs/"
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(os.path.join(path, name), "w", encoding='utf-8') as file:
            for item in comments:
                file.write(item)
            file.write(problem_line)
            for item in edge_line_list:
                file.write(item)

    def _read_from_graph(self, graph_filename):
        """This function reads graph information
        from .graph file by using the "read_file"
        function in GraphReader-object.

        Args:
            graph_filename (str): name for the file that needs reading

        Returns:
            tuple: name, number of nodes, number or edges, comments and edges
        """
        graph_info = self.graph_reader.read_file(graph_filename)
        name = graph_info[0]
        no_of_nodes = graph_info[1]
        no_of_edges = graph_info[2]
        comments_for_conversion = graph_info[5]
        edges = graph_info[6]
        return (name, no_of_nodes, no_of_edges, comments_for_conversion, edges)

    def _process_comments(self, comments, edge_string):
        """This function processes comments read from .graph file
        so that they can be inserted in the DIMACS file.

        Args:
            comments (str): comments read from .graph file
            edge_string (str): list of edges as comments in order
            to include the weights

        Returns:
        list: comment lines for DIMACS
        """
        processed_comments = []
        for item in comments:
            item = item.lstrip("# ")
            item = "c "+item
            processed_comments.append(item)
        processed_comments.append("c List of edges with weights: "+edge_string+"\n")
        return processed_comments

    def _process_edges(self, edges):
        """This function processes edges read from .graph file
        so that they can be inserted in the DIMACS file.

        Args:
            edges (list?): edges of the graph

        Returns:
            tuple: list of edges without weights as sets of two nodes,
            edges with weights as a single string
        """
        all_edges = []
        edge_string = ""
        for item in edges:
            item = item.rstrip("\n")
            edge_string +="e "+item+", "
            node1, node2, weight = item.split()
            edge = {node1, node2}
            if not edge in all_edges:
                # one edge can appear in a DIMACS file only once
                all_edges.append(edge)
        edge_string = edge_string[0:-2]
        return all_edges, edge_string

    def _create_edge_line_list(self, processed_edges):
        """This function creates the edges lines for the DIMACS file.

        Args:
            processed_edges (list): edges as sets of two nodes

        Returns:
            list: single edge line strings that can be inserted in the
            DIMACS file
        """
        edge_line_list = []
        for edge in processed_edges:
            edge_string = "e "
            for node in edge:
                edge_string+=" "+str(node)
            edge_string+="\n"
            edge_line_list.append(edge_string)
        return edge_line_list
