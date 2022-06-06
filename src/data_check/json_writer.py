import json

class JsonWriter:

    def __init__(self):
        pass

    def create_json_file(self, dataset, name, sh_desc, long_desc, licence):
        dataset_dict = {
            "name" : name,
            "descr_short" : sh_desc,
            "descr_long" : long_desc,
            "licence" : licence
        }
        with open (self.get_json_path(dataset), "w") as file:
            json.dump(dataset_dict, file)

    def update_json_file(self, dataset, key, value):
        json_path = self.get_json_path(dataset)
        new_info = {key : value}
        with open(json_path, "r+") as file:
            data = json.load(file)
            data.update(new_info)
            file.seek(0)
            json.dump(data, file)

    def get_json_path(self, dataset):
        path = dataset.get_path()
        return path+"/description.json"