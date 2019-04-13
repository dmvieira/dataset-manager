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
                    ds_metadata["identifier"] = ".".join(dataset.split(".")[:-1])
                    datasets.append(ds_metadata)
        return pd.DataFrame(datasets)
            
    def get_dataset(self, identifier, *args, **kwargs):
        datasets = self.list_datasets()
        dataset = datasets[datasets.identifier == identifier]
        dataset_format = dataset.format.values[0]
        dataset_source = dataset.source.values[0]
        read_function = "read_{}".format(dataset_format)
        if read_function in dir(pd):
            return eval("pd.{}".format(read_function))(dataset_source, *args, **kwargs)
        else:
            raise NotImplementedError("Pandas function {} not found".format(read_function))
    
    def create_dataset(self, identifier, source, description, format_extension):
        dataset = {
            "source": source,
            "description": description,
            "format": format_extension
        }
        dataset_path = os.path.join(self.__dataset_path, identifier)
        with open("{}.yaml".format(dataset_path), "w") as dataset_file:
            yaml.dump(dataset, dataset_file)
    
    def remove_dataset(self, identifier):
        dataset_path = os.path.join(self.__dataset_path, identifier)
        if os.path.isfile("{}.yaml".format(dataset_path)):
            os.remove("{}.yaml".format(dataset_path))
        else:
            datasets = self.list_datasets()
            identifiers = ", ".join(datasets.identifier.values.tolist())
            raise IOError("No dataset identifier {}. Just: {}".format(identifier, identifiers))
