class Dataset:
    """This class creates a dataset object that has a list of graphs as a parameter."""
    def __init__(self, graphs):
        """This function initializes the dataset object.

        Args:
            graphs (list): list of graph objects
        """
        self.graphs = graphs

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
