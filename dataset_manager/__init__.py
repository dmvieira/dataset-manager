"""dataset_manager
module to manage datasets
"""
import os
import yaml
from dataset_manager.data_source import DataSource

class DatasetManager(object):
    "Class to parse the config files and handle the datasets"
    def __init__(self, dataset_path):
        self.__dataset_path = dataset_path
        datasets = self.__get_datasets(dataset_path)
        self.__datasets = datasets
        self.__datasources = self.__get_data_sources(datasets)

    def get_datasets(self):
        "gets a dict with all datasets, where the key is the identifier"
        self.__datasets = self.__get_datasets(self.__dataset_path)
        return self.__datasets

    def get_dataset(self, identifier):
        "gets a dataset config by name"
        datasets = self.get_datasets()
        dataset = datasets.get(identifier)
        if dataset:
            return dataset

        identifiers = datasets.keys()
        raise IOError("No dataset identifier {}. Just: {}".format(identifier, identifiers))


    def create_dataset(self, identifier, source, description, **kwargs):
        "creates a dataset config file"
        dataset_dict = {
            "source": source,
            "description": description
            }
        dataset_dict.update(kwargs)
        dataset_path = os.path.join(self.__dataset_path, identifier)
        with open("{}.yaml".format(dataset_path), "w") as dataset_file:
            yaml.dump(dataset_dict, dataset_file)

    def remove_dataset(self, identifier):
        "removes a dataset config file"
        dataset_path = os.path.join(self.__dataset_path, identifier)
        file_to_delete = "{}.yaml".format(dataset_path)
        if os.path.isfile(file_to_delete):
            os.remove(file_to_delete)
        else:
            identifiers = self.get_datasets()
            raise IOError("No dataset identifier {}. Just: {}".format(identifier, identifiers))

    def prepare_dataset(self):
        "download and unzip all datasets"
        for k in self.__datasources:
            datasource = self.__datasources[k]
            datasource.download()
            datasource.unzip_file()

    def load_as_pandas(self, identifier, *args, **kargs):
        "read a dataset using pandas and return a dataframe"
        datasource = self.__datasources[identifier]
        return datasource.load_as_pandas(*args, **kargs)

    def __get_config_files(self, dataset_path):
        all_files = os.listdir(dataset_path)
        yaml_files = [os.path.join(dataset_path, yaml_f) for yaml_f in all_files if yaml_f.endswith(".yaml")]
        return yaml_files

    def __parser_config_file(self, file):
        result = {}
        with open(file, "r") as conf_f:
            ds_metadata = yaml.load(conf_f, Loader=yaml.FullLoader)
            file_name = os.path.split(file)[-1]
            identifier = file_name.split(".")[0]
            result = {identifier : ds_metadata}
        return result

    def __get_datasets(self, config_path):
        datasets = {}
        config_files = self.__get_config_files(config_path)
        for config_file in config_files:
            datasets.update(self.__parser_config_file(config_file))
        return datasets

    def __get_data_sources(self, datasets):
        data_source = {}
        for k in datasets:
            dataset = datasets[k]
            source = dataset["source"]
            description = dataset["description"]
            read_format = dataset.get("format", "csv")
            local_source = dataset.get("local_source")
            data_source[k] = DataSource(k, source, description, read_format, local_source)
        return data_source
