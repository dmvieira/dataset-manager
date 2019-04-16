import os
import pandas as pd
import yaml

class DatasetManager(object):
    def __init__(self, dataset_path):
        self.__dataset_path = dataset_path
#        self.__datasource_list = self.__get_data_sources()

    def list_datasets(self):
        datasets = []
        config_files = self.__get_config_files()
        for config_file in config_files:
            datasets.append(self.__parser_config_file(config_file))
        return pd.DataFrame(datasets)
    
    def __get_config_files(self):
        all_files = os.listdir(self.__dataset_path)
        yaml_files = [os.path.join(self.__dataset_path, yaml_f) for yaml_f in all_files if yaml_f.endswith(".yaml")]
        return yaml_files

    def __parser_config_file(self,file):
        with open(file, "r") as f:
            ds_metadata = yaml.load(f, Loader=yaml.FullLoader)
            file_name = os.path.split(file)[-1]
            ds_metadata["identifier"] = file_name.split(".")[0]
            return ds_metadata

    def get_dataset(self, identifier):
        datasets = self.list_datasets()
        dataset = datasets[datasets.identifier == identifier]
        if dataset.shape[0] > 0:
            return dataset.to_dict('records')[0]
        else:
            identifiers = self.__get_available_identifiers()
            raise IOError("No dataset identifier {}. Just: {}".format(identifier, identifiers))
    
    def __get_available_identifiers(self):
        datasets = self.list_datasets()
        identifiers = ", ".join(datasets.identifier.values.tolist())
        return identifiers

    def create_dataset(self, identifier, source, description, **kwargs):
        dataset = {
            "source": source,
            "description": description
        }
        dataset.update(kwargs)
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
