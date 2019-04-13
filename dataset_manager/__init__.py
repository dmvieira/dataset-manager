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
            
    def get_dataset(self, identifier):
        datasets = self.list_datasets()
        dataset = datasets[datasets.identifier == identifier]
        if dataset.shape[0] > 0:
            dataset_source = dataset.source.values[0]
            return dataset_source
        else:
            identifiers = self.__get_available_identifiers()
            raise IOError("No dataset identifier {}. Just: {}".format(identifier, identifiers))
    
    def __get_available_identifiers(self):
        datasets = self.list_datasets()
        identifiers = ", ".join(datasets.identifier.values.tolist())
        return identifiers

    def create_dataset(self, identifier, source, description):
        dataset = {
            "source": source,
            "description": description
        }
        dataset_path = os.path.join(self.__dataset_path, identifier)
        with open("{}.yaml".format(dataset_path), "w") as dataset_file:
            yaml.dump(dataset, dataset_file)
    
    def remove_dataset(self, identifier):
        dataset_path = os.path.join(self.__dataset_path, identifier)
        if os.path.isfile("{}.yaml".format(dataset_path)):
            os.remove("{}.yaml".format(dataset_path))
        else:
            identifiers = self.__get_available_identifiers()
            raise IOError("No dataset identifier {}. Just: {}".format(identifier, identifiers))
