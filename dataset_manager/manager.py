# -*- coding: utf-8 -*
"""Dataset Manager

This module helps to administrate the datasource
for a DataScience projetc.

"""
import os
import logging
import yaml
import pandas as pd
from fs.osfs import OSFS

from dataset_manager.dataset import DataSet
from dataset_manager.printer import Printer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - '
        '%(name)s - '
        '%(funcName)s - '
        '%(levelname)s - '
        '%(message)s',
    datefmt='%m-%d %H:%M')

class DatasetManager:
    """DatasetManager is the class to administrate the datasources
    from a project.

    It is required a path with all datasource configurations as
    yaml files.

    Each file represents a datadource and must have the attributes:
    `source`, `description`, `format` and
    `local_path`(to save the downloaded data).

    Args:
        dataset_path: path to the datasets configurations.
    """
    def __init__(self, dataset_path, local_path="/tmp", fs=OSFS(".")):
        self.__fs = fs
        self.__dataset_path = dataset_path
        self.__local_path = local_path
        self.__logger = logging.getLogger(
            self.__class__.__name__)

    def get_datasets(self):
        """Returns a dict with all datasets informations.

        Returns:
            dict: The key is the identifier and the value is a dict
            with the configurations. The identifier is the name of the
            configuration file.
        """

        datasets = self.__get_datasets()
        dataset = {}
        for k in datasets:
            d = datasets[k]
            source = d.pop("source")
            description =  d.pop("description")
            compression = d.pop("compression", None)
            dataset[k] = DataSet(self.__fs, os.path.join(self.__local_path, k), k, source, description, compression, **d)
        return dataset
    
    def get_dataset(self, identifier):
        """Gets a dataset config by name.

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
        """Return all datasets configurations as string table

        Returns:
            PTable: Printable table in html or ascii
        """
        return Printer(self.get_datasets())

    def create_dataset(self, identifier, source, description, format=None, compression=None, **kwargs):
        """Creates a dataset config file.

        Args:
            identifier: name to identify the dataset.
            source: path or url where the dataset is in.
            description: description about the dataset.
            **kwargs: extra attributer to save in configuration file.
        """
        dataset_dict = {
            "source": source,
            "description": description,
            "format": format,
            "compression": compression
            }
        dataset_dict.update(kwargs)
        dataset_dict = {k: v for k, v in dataset_dict.items() if v is not None}
        self.__logger.info("dataset attributes: \n {}".format(dataset_dict))
        dataset_path = os.path.join(self.__dataset_path, identifier)
        with self.__fs.open("{}.yaml".format(dataset_path), "w") as dataset_file:
            yaml.dump(dataset_dict, dataset_file)

    def remove_dataset(self, identifier):
        """Removes a dataset config file.

        Args:
            identifier: name to identify the dataset.

        Raise:
            IOError: In case of nonexistent identifier.
        """
        dataset_path = os.path.join(self.__dataset_path, identifier)
        file_to_delete = "{}.yaml".format(dataset_path)
        if self.__fs.isfile(file_to_delete):
            self.__fs.remove(file_to_delete)
            self.__logger.info("delete dataset {}".format(identifier))
        else:
            identifiers = self.get_datasets()
            raise IOError("No dataset identifier {}. Just: {}".format(identifier, identifiers))

    def prepare_datasets(self):
        """Download and unzip all datasets."""
        all_datasources = self.get_datasets()
        for k in all_datasources:
            self.__logger.info("Preparing {} ...".format(k))
            datasource = all_datasources[k]
            datasource.prepare()
            self.__logger.info("{} is ready to use!".format(k))

    def __get_datasets(self):

        datasets = {}
        config_files = self._get_config_files()
        for config_file in config_files:
            datasets.update(self._parser_config_file(config_file))
        return datasets

    def _get_config_files(self):
        all_files = self.__fs.listdir(self.__dataset_path)
        all_yaml = [yaml for yaml in all_files if yaml.endswith(".yaml")]
        abs_yaml_files = [os.path.join(self.__dataset_path, yaml_f) for yaml_f in all_yaml]
        return abs_yaml_files

    def _parser_config_file(self, file):
        result = {}
        with self.__fs.open(file, "r") as conf_f:
            ds_metadata = yaml.load(conf_f, Loader=yaml.FullLoader)
            file_name = os.path.split(file)[-1]
            identifier = file_name.split(".")[0]
            result = {identifier : ds_metadata}
        return result

