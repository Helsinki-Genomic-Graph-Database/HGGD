class Calculator:
    "This class makes calculations for datasets."
    def __init__(self):
        pass

    def get_no_nodes_and_edges(self, dataset):
        """This function calculates the number of nodes and edges in
        all the graphs of one dataset.

        Args:
            dataset (dataset object): dataset of graphs

        Returns:
            tuple: number of nodes, number of edges
        """
        graphs = dataset.get_graphs()
        total_nodes = 0
        total_edges = 0
        for graph in graphs:
            no_nodes = graph.get_nodes()
            no_edges = graph.get_edges()
            total_nodes += no_nodes
            total_edges += no_edges
        return total_nodes, total_edges

    def calculate_statistics(self, dataset):
        """This function calculates the total amount of graphs in a dataset
        and the average number of nodes and edges in a dataset."""
        graphs_total = len(dataset.get_graphs())
        number_nodes, number_edges = self.get_no_nodes_and_edges(dataset)
        avg_nodes = round(number_nodes / graphs_total)
        avg_edges = round(number_edges / graphs_total)
        return graphs_total, avg_nodes, avg_edges
