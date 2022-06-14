import os
from src.website_creator.graph_reader import GraphReader

class DimacsConverter:
    def __init__(self, directory):
        self.dir = directory
        self.graph_reader = GraphReader(self.dir)

    def convert_graph_to_dimacs(self, graph_filename):
        name, no_of_nodes, no_of_edges, comments_for_conversion, edges = self.read_from_graph(graph_filename)
        name = name+".dimacs"
        processed_edges, edge_string = self.process_edges(edges)
        comments = self.process_comments(comments_for_conversion, edge_string)
        problem_line = "p edge "+str(no_of_nodes)+" "+str(no_of_edges)+"\n"
        edge_line_list = self. create_edge_line_list(processed_edges)
        self.write_dimacs_file(name, comments, problem_line, edge_line_list)

    def write_dimacs_file(self, name, comments, problem_line, edge_line_list):
        with open(os.path.join(self.dir, name), "w", encoding='utf-8') as file:
            for item in comments:
                file.write(item)
            file.write(problem_line)
            for item in edge_line_list:
                file.write(item)

    def read_from_graph(self, graph_filename):
        graph_info = self.graph_reader.read_file(graph_filename)
        name = graph_info[0]
        no_of_nodes = graph_info[1]
        no_of_edges = graph_info[2]
        comments_for_conversion = graph_info[5]
        edges = graph_info[6]
        return (name, no_of_nodes, no_of_edges, comments_for_conversion, edges)

    def process_comments(self, comments, edge_string):
        processed_comments = []
        for item in comments:
            item = item.lstrip("# ")
            item = "c "+item
            processed_comments.append(item)
        processed_comments.append("c List of edges with weights: "+edge_string+"\n")
        return processed_comments

    def process_edges(self, edges):
        all_edges = []
        edge_string = ""
        for item in edges:
            item = item.rstrip("\n")
            edge_string +="e "+item+", "
            node1, node2, weight = item.split()
            edge = {node1, node2}
            if not edge in all_edges:
                all_edges.append(edge)
        edge_string = edge_string[0:-2]
        return all_edges, edge_string

    def create_edge_line_list(self, processed_edges):
        edge_line_list = []
        for edge in processed_edges:
            edge_string = "e "
            for node in edge:
                edge_string+=" "+str(node)
            edge_string+="\n"
            edge_line_list.append(edge_string)
        return edge_line_list
