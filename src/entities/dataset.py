class Dataset:
    """This class creates a dataset object that holds all the information on the dataset."""
    def __init__(self, description_file_exists = False, data_exists = False, licence_file_exists = False, \
            path = "", name = "", descr_short = "", descr_long = "", licence ="", show_on_website = False, \
            folder_name = "", user_defined_columns = None, has_log_file = False):
        """This function initializes the dataset object."""
        self.folder_name = folder_name
        self.description_file_exists = description_file_exists
        self.data_exists = data_exists
        self.licence_file_exists = licence_file_exists
        self.path = path
        self.name = name
        self.descr_short = descr_short
        self.descr_long = descr_long
        self.licence = licence
        self.zipfile_path = f"{self.folder_name}.zip"
        self.list_of_graphs = None
        self.dataset_source = None
        self.total_edges = None
        self.total_nodes = None
        self.average_edges = None
        self.average_nodes = None
        self.number_of_graphs =  None
        self.show_on_website = show_on_website
        self.user_defined_columns = user_defined_columns
        self.has_log_file = has_log_file

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        if self.name is None or other.name is None:
            return False
        return self.name.lower() < other.name.lower()

    def get_folder_name(self):
        return self.folder_name

    def get_description_file_exists(self):
        return self.description_file_exists

    def get_data_exists(self):
        return self.data_exists

    def get_licence_file_exists(self):
        return self.licence_file_exists

    def get_path(self):
        return self.path

    def get_name(self):
        return self.name

    def get_descr_short(self):
        return self.descr_short

    def get_descr_long(self):
        return self.descr_long

    def get_descr_long_for_dataset_html(self):
        """ Returns long description if available
        othewise uses short description

        Returns:
            str: description
        """
        if self.descr_long == None:
            return self.descr_short
        if len(self.descr_long) > 0:
            return self.descr_long
        return self.descr_short

    def get_licence(self):
        return self.licence

    def get_zipfile_path(self):
        return self.zipfile_path

    def get_list_of_graphs(self):
        return self.list_of_graphs

    def get_dataset_source(self):
        return self.dataset_source

    def get_total_edges(self):
        return self.total_edges

    def get_total_nodes(self):
        return self.total_nodes

    def get_average_edges(self):
        return self.average_edges

    def get_average_nodes(self):
        return self.average_nodes

    def get_number_of_graphs(self):
        return self.number_of_graphs

    def get_show_on_website(self):
        return self.show_on_website

    def get_user_defined_columns(self):
        return self.user_defined_columns

    def get_has_log_file(self):
        return self.has_log_file

    def set_folder_name(self, folder_name):
        self.folder_name = folder_name

    def set_description_file_exists(self, description_file_exists):
        self.description_file_exists = description_file_exists

    def set_data_exists(self, data_exists):
        self.data_exists = data_exists

    def set_licence_file_exists(self, licence_file_exists):
        self.licence_file_exists = licence_file_exists

    def set_path(self, path):
        self.path = path

    def set_name(self, name):
        self.name = name

    def set_descr_short(self, descr_short):
        self.descr_short = descr_short

    def set_descr_long(self, descr_long):
        self.descr_long = descr_long

    def set_licence(self, licence):
        self.licence = licence

    def set_zipfile_path(self, zipfile_path):
        self.zipfile_path = zipfile_path

    def set_list_of_graphs(self, list_of_graphs):
        self.list_of_graphs = list_of_graphs

    def set_dataset_source(self, dataset_source):
        self.dataset_source = dataset_source

    def set_total_edges(self, total_edges):
        self.total_edges = total_edges

    def set_total_nodes(self, total_nodes):
        self.total_nodes = total_nodes

    def set_average_edges(self, average_edges):
        self.average_edges = average_edges

    def set_average_nodes(self, average_nodes):
        self.average_nodes = average_nodes

    def set_number_of_graphs(self, number_of_graphs):
        self.number_of_graphs = number_of_graphs

    def set_show_on_website(self, show_on_website):
        self.show_on_website = show_on_website

    def set_user_defined_columns(self, user_defined_columns):
        self.user_defined_columns = user_defined_columns

    def set_has_log_file(self, has_log_file):
        self.has_log_file = has_log_file

    def find_graph(self, name):
        """ This function returns a specific graph

        Args:
            name (string): name of graph

        Returns:
            graph-object
        """
        for graph in self.list_of_graphs:
            if graph.get_names() == name:
                return graph
        return None

    def get_statistics(self):
        """ Returns all statistics at once

        Returns:
            _type_: _description_
        """
        return self.number_of_graphs, self.average_nodes, self.average_edges, \
            self.total_nodes, self.total_edges
