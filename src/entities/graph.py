class Graph:
    """This class creates a graph object that has the name
    of the graph, the number of nodes and the number of edges."""
    def __init__(self, name = "", nodes = 0, edges = 0, sources = [], licence = None, \
        file_name = "", file_format = "", short_desc = None, user_defined_columns = None, \
        description_file_exists = False):
        """This function initializes the graph object.

        Args:
            name (string): name of the graph
            nodes (integer): number of nodes
            edges (integer): number of edges
            sources (list of tuples): list of links source files and source file names for the graph
            licence (string): licence for the graph
        """
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.sources = sources
        self.licence = licence
        self.file_name = file_name
        self.file_format = file_format
        self.short_desc = short_desc
        self.user_defined_columns = user_defined_columns
        self.description_file_exists = description_file_exists

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        """ To sort graphs by name

        """
        if self.name is None or other.name is None:
            return False
        return self.name.lower() < other.name.lower()

    def get_names(self):
        """This function returns the name of the graph.

        Returns:
            string: name
        """
        return self.name

    def get_user_defined_columns(self):
        return self.user_defined_columns

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

    def get_licence(self):
        return self.licence

    def get_file_name(self):
        return self.file_name

    def get_file_format(self):
        return self.file_format

    def get_short_desc(self):
        return self.short_desc

    def get_description_file_exists(self):
        return self.description_file_exists

    def set_description_file_exists(self, description_file_exists):
        self.description_file_exists = description_file_exists

    def set_file_format(self, file_format):
        self.file_format = file_format

    def set_licence(self, licence):
        self.licence = licence

    def set_name(self, name):
        self.name = name

    def set_sources(self, sources):
        self.sources = sources

    def set_nodes(self, nodes):
        self.nodes = nodes

    def set_edges(self, edges):
        self.edges = edges

    def set_filename(self, filename):
        self.file_name = filename

    def set_short_desc(self, desc):
        self.short_desc = desc

    def set_user_defined_columns(self, user_defined_columns):
        self.user_defined_columns = user_defined_columns
