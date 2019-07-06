import os
import unittest
import yaml
from fs.osfs import OSFS

from dataset_manager import DatasetManager

class TestDatasetManager(unittest.TestCase):

    trash_dir = "./tests/resources/trash_data"

    def setUp(self):
        self.os = OSFS(".")

    def tearDown(self):
        for data in self.os.listdir(self.trash_dir):
            if data != ".keep":
                self.os.remove("{}/{}".format(self.trash_dir, data))
        self.os.close()

    def test_should_read_yaml_from_dir(self):

        expected = {
            "one_test" : {
                "source": "http://source/teste",
                "description": "my little dataset"
                }
            }

        data = DatasetManager("./tests/resources/one_data")
        self.assertDictEqual(data.get_datasets(), expected)
    

    def test_should_read_multiple_yaml_from_dir(self):

        expected ={
            "one_test" : {
                "source": "https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv",
                "description": "my little dataset"
            },

            "two_test" : {
                "source": "https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv",
                "description": "my little dataset 2"

            }
        }
 
        data = DatasetManager("./tests/resources/multiple_data", fs=self.os)
        result = list(data.get_datasets().keys())
        result.sort()
        expected = ["one_test", "two_test"]
        self.assertListEqual(expected,result)

    def test_should_get_dataset(self):

        data = DatasetManager("./tests/resources/local_data")
        dataset = {"local_test" : {
            "source": "./tests/resources/local_data/train.csv",
            "description": "my little dataset local"
            }
        }
        self.assertDictEqual(data.get_dataset("local_test"), dataset.get("local_test"))

    def test_should_get_dataset_unknown(self):

        data = DatasetManager("./tests/resources/local_data")
        with self.assertRaises(IOError):
            data.get_dataset("unknown_test")
    
    def test_should_create_dataset(self):
        data = DatasetManager(self.trash_dir, fs=self.os)
        identifier = "data_name"
        dataset = {
            "identifier": identifier,
            "description": "description",
            "source": "/tmp/test.csv",
        }

        data.create_dataset(**dataset)

        loaded_datasets = data.get_datasets()
        dataset_config = loaded_datasets.get(identifier)

        self.assertTrue(self.os.isfile("{}/{}.yaml".format(self.trash_dir, identifier)))
        self.assertEqual(len(self.os.listdir(self.trash_dir)), 2)

        self.assertEqual(list(loaded_datasets.keys())[0], identifier)
        self.assertEqual(dataset_config.get("description"), dataset["description"])
        self.assertEqual(dataset_config.get("source"), dataset["source"])

    def test_should_create_dataset_with_custom_data(self):
        data = DatasetManager(self.trash_dir, fs=self.os)
        identifier = "data_name_custom"
        dataset = {
            "identifier": identifier,
            "description": "description",
            "source": "/tmp/test.csv"
        }
        data.create_dataset(**dataset)
        self.assertTrue(self.os.isfile("{}/{}.yaml".format(self.trash_dir, identifier)))
      
        self.assertEqual(len(os.listdir(self.trash_dir)), 2)
        loaded_dataset = data.get_datasets()
        self.assertEqual(list(loaded_dataset.keys()), [identifier])

        datasource_configs = loaded_dataset.get(identifier)
        self.assertEqual(datasource_configs["description"], dataset["description"])
        self.assertEqual(datasource_configs["source"], dataset["source"])


    def test_should_remove_dataset(self):
        data = DatasetManager(self.trash_dir, fs=self.os)
        identifier = "data_name"
        dataset = {
            "identifier": identifier,
            "description": "description",
            "source": "/tmp/test.csv"
        }
        data.create_dataset(**dataset)
        self.assertTrue(os.path.isfile("{}/{}.yaml".format(self.trash_dir, identifier)))
        self.assertEqual(len(os.listdir(self.trash_dir)), 2)
        data.remove_dataset(identifier)
        self.assertFalse(os.path.isfile("{}/{}.yaml".format(self.trash_dir, identifier)))
        self.assertEqual(len(os.listdir(self.trash_dir)), 1)

    def test_should_remove_unknown_dataset(self):

        data = DatasetManager("./tests/resources/local_data", fs=self.os)
        with self.assertRaises(IOError):
            data.remove_dataset("unknown_dataset")
