from src.website_creator.graph_creator import GraphCreator
from src.website_creator.calculator import calculator_service

class ReadGraphs:
    """ Updates the dataset list with graphs, sources
       and the statistics from the graphss
    """
    def __init__(self, dataset_list):
        self.dataset_list = dataset_list
        self.updated_dataset_list = []

    def run(self):
        """ Checks every dataset in dataset list and updates the info
            Shows only those approved for appear on website
        """
        for dataset in self.dataset_list:
            if dataset.get_show_on_website():
                graphcreator_service = GraphCreator(dataset.get_path(), dataset.get_licence(), \
                    dataset.get_licence_file_exists())
                graphcreator_service.run()
                dataset.set_list_of_graphs(graphcreator_service.get_graph_list())
                dataset.set_dataset_source(graphcreator_service.get_set_sources())
                total_nodes, total_edges = calculator_service.get_no_nodes_and_edges(dataset)
                dataset.set_total_nodes(total_nodes)
                dataset.set_total_edges(total_edges)
                nro_graphs, avg_nodes, avg_edges = calculator_service.calculate_statistics(dataset)
                dataset.set_number_of_graphs(nro_graphs)
                dataset.set_average_nodes(avg_nodes)
                dataset.set_average_edges(avg_edges)
                self.updated_dataset_list.append(dataset)

    def get_dataset_list_with_graphs(self):
        """ Returns the updated dataset list

        Returns:
            list: Updated dataset list
        """
        return self.updated_dataset_list
