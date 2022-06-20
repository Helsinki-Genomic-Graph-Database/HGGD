import json

class JsonWriter:
    """This class includes methods for writing json-files."""
    def __init__(self):
        pass

    def create_json_file(self, dataset, name, sh_desc, long_desc, licence):
        """This method created a new json files or writes to an empty one.

        Args:
            dataset
            name (string)
            sh_desc (string): short description
            long_desc (string): long description
            licence (string)
        """
        dataset_dict = {
            "name" : name,
            "descr_short" : sh_desc,
            "descr_long" : long_desc,
            "licence" : licence
        }
        with open (self.get_json_path(dataset), "w", encoding='utf-8') as file:
            json.dump(dataset_dict, file, indent=4)

    def update_json_file(self, dataset, key, value):
        """This method add information to an existing json file.

        Args:
            dataset
            key (string)
            value (string)
        """
        json_path = self.get_json_path(dataset)
        new_info = {key : value}
        with open(json_path, "r+", encoding='utf-8') as file:
            data = json.load(file)
            data.update(new_info)
            file.seek(0)
            json.dump(data, file, indent=4)

    def get_json_path(self, dataset):
        path = dataset.get_path()
        return path+"/description.json"

    def get_graph_json_path(self, dataset, graph):
        dataset_folder_path = dataset.get_path()
        extension_length = len(graph.split(".")[-1])
        graph_without_extension = graph[:-extension_length-1]
        return dataset_folder_path+"/"+graph_without_extension+"_description.json"

    def create_graph_description(self, dataset, graph, short_desc):
        dataset_dict = {
            "descr_short" : short_desc
        }
        with open (self.get_graph_json_path(dataset, graph), "w", encoding='utf-8') as file:
            json.dump(dataset_dict, file, indent=4)

    def update_graph_description(self, dataset, graph, short_desc):
        json_path = self.get_graph_json_path(dataset, graph)
        new_info = {"descr_short" : short_desc}
        with open(json_path, "r+", encoding='utf-8') as file:
            data = json.load(file)
            data.update(new_info)
            file.seek(0)
            json.dump(data, file, indent=4)
