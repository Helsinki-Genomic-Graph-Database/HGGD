class Graph:
    """This class creates a graph object that has the name
    of the graph, the number of nodes and the number of edges."""
    def __init__(self, name = "", nodes = 0, edges = 0, sources = []):
        """This function initializes the graph object.

        Args:
            name (string): name of the graph
            nodes (integer): number of nodes
            edges (integer): number of edges
        """
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.sources = sources

    def get_names(self):
        """This function returns the name of the graph.

        Returns:
            string: name
        """
        return self.name

    def get_nodes(self):
        """This function returns the number of nodes in the graph.

        Returns:
            integer: nodes
        """
        return self.nodes

    def get_edges(self):
        """This function returns the number of edges in the graph.

        Returns:
            integer: edges
        """
        return self.edges

    def get_sources(self):
        return self.sources
