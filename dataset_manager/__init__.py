import os
import pandas as pd
import yaml

class DatasetManager(object):
    def __init__(self, dataset_path):
        self.__dataset_path = dataset_path
        self.datasets = self.list_datasets()
    
    def list_datasets(self):
        datasets = []
        for dataset in os.listdir(self.__dataset_path):
            if dataset.endswith(".yaml"):
                dataset_path = os.path.join(self.__dataset_path, dataset)
                with open(dataset_path, "r") as dataset_file:
                    datasets.append(yaml.load(dataset_file, Loader=yaml.FullLoader))
        return pd.DataFrame(datasets)
            
    def get_dataset(self, name, *args, **kwargs):
        dataset = self.datasets[self.datasets.name == name]
        dataset_format = dataset.format.values[0]
        dataset_src = dataset.src.values[0]
        read_function = "read_{}".format(dataset_format)
        if read_function in dir(pd):
            return eval("pd.{}".format(read_function))(dataset_src, *args, **kwargs)
        else:
            raise NotImplementedError("Pandas function {} not found".format(read_function))
