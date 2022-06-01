class Dataset:
    """This class creates a dataset object that has a list of graphs as a parameter."""
    def __init__(self, datasetpath, name, graphs, descr_short = "", descr_long = "", licence="", foldername="", sources = [], has_licence_files=False):
        """This function initializes the dataset object.

        Args:
            name (str): name of the dataset
            graphs (list): list of graph objects
        """
        self.name = name
        self.graphs = graphs
        self.descr_short = descr_short
        self.descr_long = descr_long
        self.licence = licence
        self.foldername = foldername.strip().split("/")[-1]
        self.sources = sources
        self.has_licence_files = has_licence_files
        self.datasetpath = datasetpath

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
        return None

    def get_name(self):
        return self.name

    def get_descr_short(self):
        return self.descr_short

    def get_descr_long(self):
        """ Returns long description if available
        othewise uses short description

        Returns:
            str: description
        """
        if len(self.descr_long) > 0:
            return self.descr_long
        return self.descr_short

    def get_foldername(self):
        return self.foldername

    def get_licence(self):
        return self.licence

    def get_sources(self):
        return self.sources

    def get_has_licence_files(self):
        return self.has_licence_files

    def get_datasetpath(self):
        return self.datasetpath