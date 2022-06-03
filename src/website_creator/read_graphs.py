from src.website_creator.graph_reader import GraphReader
from src.website_creator.calculator import calculator_service

class ReadGraphs:
    def __init__(self, dataset_list):
        self.dataset_list = dataset_list

    def run(self):
        for dataset in self.dataset_list:
            graphreader_service = GraphReader(dataset.get_path(), dataset.get_licence(), dataset.get_licence_file_exists())
            graphreader_service.run()
            dataset.set_list_of_graphs() = graphreader_service.get_graph_list()
            dataset.set.dataset_source() = graphreader_service.get_set_sources()
            dataset.set_total_nodes(), dataset.set_total_edges() = calculator_service.get_no_nodes_and_edges(dataset)
            dataset.set_number_of_graphs(), dataset.set_average_nodes(), dataset.set_average_edges() = calculator_service.calculate_statistics(dataset)

    def get_dataset_list_with_graphs(self):
        return self.dataset_list
