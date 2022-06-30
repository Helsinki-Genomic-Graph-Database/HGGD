import os
import json
from src.file_ui.file_utils import check_file_extension, check_file_extension_multiple, check_field, read_description, read_graph_description,create_source_txt_file
from src.entities.dataset import Dataset
from src.entities.graph import Graph
from src.dataset_services.graph_reader import GraphReader
from src.dataset_services.gfa_reader import GfaReader
from src.dataset_services.dimacs_reader import DimacsReader
from src.dataset_services.calculator import calculator_service

class FolderReader:

    """
    Reads a folder and makes a Dataset object from the contents
    """

    def __init__(self, path, spdx_service):

        self.path = path
        self.files = os.listdir(path)
        self.spdx_service = spdx_service
        self.descrition_file_exists = False
        self.data_exists = False
        self.licence_file_exists = False
        self.name = None
        self.descr_short = None
        self.descr_long = None
        self.licence = set()
        self.user_defined_columns = None
        self.show_on_website = False
        self.folder_name = path.split("/")[-1]
        self.highest_modification_time = 0
        self.logtime = 0
        self.has_log_file = False
        self.sources = set()
        self.graph_list = []


        self.licence_in_descr = None

    def read_graph(self, filename, reader):
        
        name, nodes, edges, sources, licence, comments_for_conversion, edges_listed, \
                    short_desc = reader.read_file(filename)
        return Graph(name, nodes, edges, sources, None, filename)

    def read_dimacs(self, filename, dimacsreader):
        name, nodes, edges, sources, licence, short_desc \
                    = dimacsreader.read_dimacs_graph(filename)
                
        graph = Graph(name)
        graph.set_nodes(nodes)
        graph.set_edges(edges)
        graph.set_filename(filename)
        return graph

    def update_sources(self):
        for graph in self.graph_list:
            self.sources.update(graph.get_sources())

    def read_dataset_description_file(self):
        self.descrition_file_exists = True
        self.name, self.descr_short, self.descr_long, licence_in_descr, self.user_defined_columns, \
            sources = read_description(self.path)
        self.sources.update(sources)
        if not licence_in_descr is None:
            self.licence_in_descr = licence_in_descr
            licence_in_descr = self.spdx_service.create_licence_link_tuples(licence_in_descr)
            self.licence.update([licence_in_descr])
        
    def update_dataset_object(self, dataset):
        dataset.set_show_on_website(self.show_on_website)
        dataset.set_list_of_graphs(self.graph_list)
        dataset.set_dataset_source(self.sources)
        total_nodes, total_edges = calculator_service.get_no_nodes_and_edges(dataset)
        nro_graphs, avg_nodes, avg_edges = calculator_service.calculate_statistics(dataset)
        dataset.set_number_of_graphs(nro_graphs)
        dataset.set_average_nodes(avg_nodes)
        dataset.set_average_edges(avg_edges)
        dataset.set_total_nodes(total_nodes)
        dataset.set_total_edges(total_edges)

    def get_dataset(self):
        graphs = []
        graph_descriptions = []
        for filename in self.files:
            self.check_modification_times(filename)

            if check_file_extension_multiple(filename, ["graph", "gfa", "dimacs"]):
                self.data_exists = True
                graphs.append(filename)
            
            if check_file_extension(filename, "json"):
                if filename == "description.json":
                    self.read_dataset_description_file()
                else:
                    split_file = filename.split(".")[:-1]
                    if (split_file[-1].split("_")[-1]) == "description":
                        graph_descriptions.append(filename[:-len("_description.json")])

        ui_run = (self.logtime >= self.highest_modification_time)
        
        if ui_run and self.data_exists:
            self.show_on_website = True

        self.process_graphs(graphs, graph_descriptions)

        new_dataset = Dataset(self.descrition_file_exists, self.data_exists, self.licence_file_exists, \
                self.path, self.name, self.descr_short, self.descr_long, sorted(self.licence), \
                self.show_on_website, self.folder_name, self.user_defined_columns, \
                self.has_log_file)

        self.update_dataset_object(new_dataset)

        if len(self.sources) > 0:
                    create_source_txt_file(new_dataset.get_path(), new_dataset.get_folder_name(), self.sources, False)

        return new_dataset

    def check_modification_times(self, file):
        modification_time = os.path.getctime(self.path+"/"+file)
        if file == "log.txt":
            self.logtime = modification_time
            self.has_log_file = True
        else:
            if modification_time > self.highest_modification_time:
                self.highest_modification_time = modification_time

    def process_graphs(self, graphs, graph_descriptions):
        for filename in graphs:
            extension_length = len(filename.split(".")[-1])
            graph_without_extension = filename[:-extension_length-1]
            
            licence = None

            if check_file_extension(filename, "graph"):
                graphreader = GraphReader(self.path)
                graph = self.read_graph(filename, graphreader)
                graph.set_file_format("graph")
                

            if check_file_extension(filename, "gfa"):
                graphreader = GfaReader(self.path)
                graph = self.read_graph(filename, graphreader)
                graph.set_file_format("gfa")
                
            if check_file_extension(filename, "dimacs"):
                dimacsreader = DimacsReader(self.path)
                graph = self.read_dimacs(filename, dimacsreader)
                graph.set_file_format("dimacs")

            
            if graph_without_extension in graph_descriptions:
                
                name, licence, sources, short_desc, user_defined_columns = read_graph_description(self.path, graph_without_extension)
                
                if name is not None:
                    graph.set_name(name)
                if sources is not None:
                    graph.set_sources(sources)
                    self.sources.update(sources)
                graph.set_short_desc(short_desc)
                graph.set_user_defined_columns(user_defined_columns)
                graph.set_description_file_exists(True)
            
            if licence is None:
                licence = self.licence_in_descr
                
            if not licence is None:
                
                licence = self.spdx_service.create_licence_link_tuples(licence)
                self.licence.update([licence])

            graph.set_licence(licence)
            self.graph_list.append(graph)
            self.update_sources()
