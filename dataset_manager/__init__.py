import os
import pandas as pd
import yaml

class DatasetManager(object):
    def __init__(self, dataset_path):
        self.__dataset_path = dataset_path
    
    def list_datasets(self):
        datasets = []
        for dataset in os.listdir(self.__dataset_path):
            if dataset.endswith(".yaml"):
                dataset_path = os.path.join(self.__dataset_path, dataset)
                with open(dataset_path, "r") as dataset_file:
                    ds_metadata = yaml.load(dataset_file, Loader=yaml.FullLoader)
                    ds_metadata["name"] = ".".join(dataset.split(".")[:-1])
                    datasets.append(ds_metadata)
        return pd.DataFrame(datasets)
            
    def get_dataset(self, name, *args, **kwargs):
        datasets = self.list_datasets()
        dataset = datasets[datasets.name == name]
        dataset_format = dataset.format.values[0]
        dataset_src = dataset.src.values[0]
        read_function = "read_{}".format(dataset_format)
        if read_function in dir(pd):
            return eval("pd.{}".format(read_function))(dataset_src, *args, **kwargs)
        else:
            raise NotImplementedError("Pandas function {} not found".format(read_function))
    
    def create_dataset(self, name, src, description, format_extension):
        dataset = {
            "src": src,
            "description": description,
            "format": format_extension
        }
        dataset_path = os.path.join(self.__dataset_path, name)
        with open("{}.yaml".format(dataset_path), "w") as dataset_file:
            yaml.dump(dataset, dataset_file)
    
    def remove_dataset(self, name):
        dataset_path = os.path.join(self.__dataset_path, name)
        if os.path.isfile("{}.yaml".format(dataset_path)):
            os.remove("{}.yaml".format(dataset_path))
        else:
            datasets = self.list_datasets()
            names = ", ".join(datasets.name.values.tolist())
            raise IOError("No dataset named {}. Just: {}".format(name, names))
