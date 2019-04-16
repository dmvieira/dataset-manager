import os
import yaml

class DatasetManager(object):
    def __init__(self, dataset_path):
        self.__dataset_path = dataset_path
        self.__datasets = self.__get_datasets(dataset_path)
#        self.__datasource_list = self.__get_data_sources()

    def list_datasets(self):
        self.__datasets = self.__get_datasets(self.__dataset_path)
        return self.__datasets

    def __get_datasets(self, config_path):
        datasets = {}
        config_files = self.__get_config_files(config_path)
        for config_file in config_files:
            datasets.update(self.__parser_config_file(config_file))
        return datasets

    def get_dataset(self, identifier):
        datasets = self.list_datasets()
        dataset = datasets.get(identifier)
        if dataset:
            return dataset
        else:
            identifiers = datasets.keys()
            raise IOError("No dataset identifier {}. Just: {}".format(identifier, identifiers))


    def create_dataset(self, identifier, source, description, **kwargs):
        dataset_dict = {
                "source": source,
                "description": description
        }
        dataset_dict.update(kwargs)
        dataset_path = os.path.join(self.__dataset_path, identifier)
        with open("{}.yaml".format(dataset_path), "w") as dataset_file:
            yaml.dump(dataset_dict, dataset_file)
    
    def remove_dataset(self, identifier):
        dataset_path = os.path.join(self.__dataset_path, identifier)
        file_to_delete = "{}.yaml".format(dataset_path)
        if os.path.isfile(file_to_delete):
            os.remove(file_to_delete)
        else:
            identifiers = self.list_datasets()
            raise IOError("No dataset identifier {}. Just: {}".format(identifier, identifiers))

    def __get_config_files(self, dataset_path):
        all_files = os.listdir(dataset_path)
        yaml_files = [os.path.join(dataset_path, yaml_f) for yaml_f in all_files if yaml_f.endswith(".yaml")]
        return yaml_files

    def __parser_config_file(self,file):
        with open(file, "r") as f:
            ds_metadata = yaml.load(f, Loader=yaml.FullLoader)
            file_name = os.path.split(file)[-1]
            id = file_name.split(".")[0]
            return {id : ds_metadata}
