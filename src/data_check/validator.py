import os

class Validator:
    """This class has method for checking whether the dataset
    include the necessary information."""
    def __init__(self):
        pass

    def check_dataset_description_file_exists(self, dataset):
        return dataset.get_description_file_exists()

    def check_data_exists(self, dataset):
        return dataset.get_data_exists()

    def check_licence_file_exists(self, dataset):
        return dataset.get_licence_file_exists()

    def check_name_exists(self, dataset):
        if (dataset.get_name()) is None:
            return False
        if len(dataset.get_name()) == 0:
            return False
        return True

    def check_dataset_descr_short_exists(self, dataset):
        if (dataset.get_descr_short()) is None:
            return False
        if len(dataset.get_descr_short()) == 0:
            return False
        return True

    def check_descr_long_exists(self, dataset):
        if (dataset.get_descr_long()) is None:
            return False
        if len(dataset.get_descr_long()) == 0:
            return False
        return True

    def check_licence_exists(self, dataset):
        if dataset.get_licence() == "None":
            return False
        if dataset.get_licence() is None:
            return False
        if len(dataset.get_licence()) == 0:
            return False

        return True

    def check_show_on_website(self, dataset):
        return dataset.get_show_on_website()

    def check_description_file_empty(self, json_path):
        return os.stat(json_path).st_size == 0

    def check_graph_short_description(self, graph):
        if graph.get_short_desc() is None:
            return False
        if graph.get_short_desc() == "":
            return False
        return True

    def check_graph_description_file_exists(self, graph):
        return graph.get_description_file_exists()

    def count_graphs_without_sources(self, dataset):
        graphs = dataset.get_list_of_graphs()
        number_of_graphs_without_sources = 0
        for graph in graphs:
            if len(graph.get_sources()) == 0:
                number_of_graphs_without_sources += 1

        return number_of_graphs_without_sources

    def count_graphs_without_licence(self, dataset):
        graphs = dataset.get_list_of_graphs()
        number_of_graphs_without_licence = 0
        for graph in graphs:
            if graph.get_licence() is None:
                number_of_graphs_without_licence += 1

        return number_of_graphs_without_licence

    def check_if_licence_in_spdx_format(self, licence_tuple):
        if licence_tuple[1] is None:
            return False
        return True
