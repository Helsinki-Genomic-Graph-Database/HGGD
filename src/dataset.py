class Dataset:
    """This class creates a dataset object that has a list of graphs as a parameter."""
    def __init__(self, name, graphs, descr_short = "", descr_long = "", foldername=""):
        """This function initializes the dataset object.

        Args:
            name (str): name of the dataset
            graphs (list): list of graph objects
        """
        self.name = name
        self.graphs = graphs
        self.descr_short = descr_short
        self.descr_long = descr_long
        self.foldername = foldername.strip().split("/")[-1]

    def get_graphs(self):
        """This function returns a list of graphs.

        Returns:
            list: list of graph objects
        """
        return self.graphs

    def find_graph(self, name):
        """ This function returns a specific graph

        Args:
            name (string): name of graph

        Returns:
            graph-object
        """
        for graph in self.get_graphs():
            if graph.get_names() == name:
                return graph

    def get_name(self):
        return self.name

    def get_descr_short(self):
        return self.descr_short

    def get_descr_long(self):
        return self.descr_long

    def get_foldername(self):
        return self.foldername
