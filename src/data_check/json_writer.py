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
            json.dump(dataset_dict, file)

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
            json.dump(data, file)

    def get_json_path(self, dataset):
        path = dataset.get_path()
        return path+"/description.json"
