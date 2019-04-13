import os
import unittest
import yaml
import pandas as pd
from dataset_manager import DatasetManager
from pandas.util.testing import assert_frame_equal


class TestDatasetManager(unittest.TestCase):

    trash_dir = "./tests/resources/trash_data"

    def tearDown(self):
        for data in os.listdir(self.trash_dir):
            if data != ".keep":
                os.remove("{}/{}".format(self.trash_dir, data))


    def test_should_read_yaml_from_dir(self):

        expected = pd.DataFrame([
            {
                "identifier": "one_test",
                "source": "https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv",
                "description": "my little dataset"
            }
        ])

        data = DatasetManager("./tests/resources/one_data")
        assert_frame_equal(data.list_datasets(), expected)
    

    def test_should_read_multiple_yaml_from_dir(self):

        expected = pd.DataFrame([
            {
                "identifier": "one_test",
                "source": "https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv",
                "description": "my little dataset"
            },
            {
                "identifier": "two_test",
                "source": "https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv",
                "description": "my little dataset 2"
            }
        ])

        data = DatasetManager("./tests/resources/multiple_data")
        assert_frame_equal(data.list_datasets().sort_values("identifier").reset_index(drop=True), expected.sort_values("identifier").reset_index(drop=True))

    def test_should_get_dataset(self):

        data = DatasetManager("./tests/resources/local_data")
        path = "./tests/resources/local_data/train.csv"
        self.assertEqual(data.get_dataset("local_test"), path)

    def test_should_get_dataset_unknown(self):

        data = DatasetManager("./tests/resources/local_data")
        with self.assertRaises(IOError):
            data.get_dataset("unknown_test")
    
    def test_should_create_dataset(self):
        data = DatasetManager(self.trash_dir)
        identifier = "data_name"
        dataset = {
            "identifier": identifier,
            "description": "description",
            "source": "/tmp/test.csv"
        }
        data.create_dataset(**dataset)
        self.assertTrue(os.path.isfile("{}/{}.yaml".format(self.trash_dir, identifier)))
        self.assertEqual(len(os.listdir(self.trash_dir)), 2)
        loaded_dataset = data.list_datasets()
        self.assertEqual(loaded_dataset.identifier.values[0], dataset["identifier"])
        self.assertEqual(loaded_dataset.description.values[0], dataset["description"])
        self.assertEqual(loaded_dataset.source.values[0], dataset["source"])

    def test_should_remove_dataset(self):
        data = DatasetManager(self.trash_dir)
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

        data = DatasetManager("./tests/resources/local_data")
        with self.assertRaises(IOError):
            data.remove_dataset("unknown_dataset")
