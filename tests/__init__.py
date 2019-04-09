import unittest
import yaml
import pandas as pd
from dataset_manager import DatasetManager


class TestDatasetManager(unittest.TestCase):

    def test_should_read_yaml_from_dir(self):

        expected = pd.DataFrame([
            {
                "name": "one_test",
                "src": "https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv",
                "description": "my little dataset",
                "format": "csv"
            }
        ])

        data = DatasetManager("./tests/resources/one_data")
        self.assertDictEqual(data.list_datasets().to_dict(), expected.to_dict())
    

    def test_should_read_multiple_yaml_from_dir(self):

        expected = pd.DataFrame([
            {
                "name": "one_test",
                "src": "https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv",
                "description": "my little dataset",
                "format": "csv"
            },
            {
                "name": "two_test",
                "src": "https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv",
                "description": "my little dataset 2",
                "format": "csv"
            }
        ])

        data = DatasetManager("./tests/resources/multiple_data")
        self.assertDictEqual(data.list_datasets().to_dict(), expected.to_dict())

    def test_should_get_dataset(self):

        data = DatasetManager("./tests/resources/local_data")
        df = pd.read_csv("./tests/resources/local_data/train.csv")
        self.assertEqual(data.get_dataset("local_test").to_dict(), df.to_dict())
    
    def test_should_get_dataset_zipped(self):

        data = DatasetManager("./tests/resources/local_data")
        df = pd.read_csv("./tests/resources/local_data/train.csv")
        self.assertEqual(data.get_dataset("local_zip_test").to_dict(), df.to_dict())

    def test_should_get_dataset_unknown_format(self):

        data = DatasetManager("./tests/resources/local_data")
        with self.assertRaises(NotImplementedError):
            data.get_dataset("unknown_test")