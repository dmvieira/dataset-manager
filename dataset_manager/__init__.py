# -*- coding: utf-8 -*
"""Dataset Manager

This module helps to administrate the datasource
for a DataScience projetc.

"""
import os
import logging
import yaml
import pandas as pd
from dataset_manager.data_source import DataSource
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - '
        '%(name)s - '
        '%(funcName)s - '
        '%(levelname)s - '
        '%(message)s',
    datefmt='%m-%d %H:%M')

def _get_config_files(dataset_path):
    all_files = os.listdir(dataset_path)
    all_yaml = [yaml for yaml in all_files if yaml.endswith(".yaml")]
    abs_yaml_files = [os.path.join(dataset_path, yaml_f) for yaml_f in all_yaml]
    return abs_yaml_files

def _parser_config_file(file):
    result = {}
    with open(file, "r") as conf_f:
        ds_metadata = yaml.load(conf_f, Loader=yaml.FullLoader)
        file_name = os.path.split(file)[-1]
        identifier = file_name.split(".")[0]
        result = {identifier : ds_metadata}
    return result

class DatasetManager:
    """DatasetManager is the class to administrate the datasources
    from a projec.

    It is required a path with all datasource configurations as
    yaml files.

    Each file represents a datadource and must have the attributes:
    `source`, `description`, `format` and
    `local_source`(to save the downloaded data).

    Args:
        dataset_path: path to the datasets configurations.
    """
    def __init__(self, dataset_path):
        self.__dataset_path = dataset_path
        self.__logger = logging.getLogger(
            self.__class__.__name__)

    def get_datasets(self):
        """returns a dict with all datasets informations.

        Returns:
            dict: The key is the identifier and the value is a dict
            with the configurations. The identifier is the name of the
            configuration file.
        """

        datasets = {}
        config_files = _get_config_files(self.__dataset_path)
        for config_file in config_files:
            datasets.update(_parser_config_file(config_file))
        return datasets

    def get_dataset(self, identifier):
        """gets a dataset config by name.

        Args:
            identifier: datasource identifier.

        Raises:
            IOError: In case of nonexistent identifier.
        """
        datasets = self.get_datasets()
        dataset = datasets.get(identifier)
        if dataset:
            return dataset

        identifiers = datasets.keys()
        raise IOError("No dataset identifier {}. Just: {}".format(identifier, identifiers))

    def show_datasets(self):
        """return all datasets configurations as pandas dataframe

        Returns:
            DataFrame: Pandas Dataframe with all datasets
        """
        datasets = self.get_datasets()
        lines = []
        for identifier in datasets:
            line = dict()
            line["identifier"] = identifier
            line.update(datasets[identifier])
            lines.append(line)
        return pd.DataFrame(lines)

    def create_dataset(self, identifier, source, description, **kwargs):
        """creates a dataset config file.

        Args:
            identifier: name to identify the dataset.
            source: path or url where the dataset is in.
            description: description about the dataset.
            **kwargs: extra attributer to save in configuration file.
        """
        dataset_dict = {
            "source": source,
            "description": description
            }
        dataset_dict.update(kwargs)
        self.__logger.info("dataset attributes: \n {}".format(dataset_dict))
        dataset_path = os.path.join(self.__dataset_path, identifier)
        with open("{}.yaml".format(dataset_path), "w") as dataset_file:
            yaml.dump(dataset_dict, dataset_file)

    def remove_dataset(self, identifier):
        """removes a dataset config file.

        Args:
            identifier: name to identify the dataset.

        Raise:
            IOError: In case of nonexistent identifier.
        """
        dataset_path = os.path.join(self.__dataset_path, identifier)
        file_to_delete = "{}.yaml".format(dataset_path)
        if os.path.isfile(file_to_delete):
            os.remove(file_to_delete)
            self.__logger.info("delete dataset {}".format(identifier))
        else:
            identifiers = self.get_datasets()
            raise IOError("No dataset identifier {}. Just: {}".format(identifier, identifiers))

    def prepare_dataset(self):
        """Download and unzip all datasets."""
        all_datasources = self.__get_data_sources()
        for k in all_datasources:
            self.__logger.info("Preparing {} ...".format(k))
            datasource = all_datasources[k]
            datasource.download()
            datasource.unzip_file()
            self.__logger.info("{} is ready to use!".format(k))

    def load_as_pandas(self, identifier, *args, **kwargs):
        """Read a dataset using pandas and return a dataframe.

        Args:
            identifier: name to identify the dataset.
            *args and **kwargs: args to pass to the pandas read function.
        """
        all_datasources = self.__get_data_sources()
        datasource = all_datasources[identifier]
        return datasource.load_as_pandas(*args, **kwargs)

    def __get_data_sources(self):
        datasets = self.get_datasets()
        data_source = {}
        for k in datasets:
            dataset = datasets[k]
            source = dataset.pop("source")
            description =  dataset.pop("description")
            read_format = dataset.pop("format", "csv")
            data_source[k] = DataSource(k, source, description, read_format, **dataset)
        return data_source
