import unittest
import yaml
import pandas as pd
from dataset_manager import DatasetManager
from pandas.util.testing import assert_frame_equal


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
        assert_frame_equal(data.list_datasets(), expected)
    

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
        assert_frame_equal(data.list_datasets().sort_values("name"), expected.sort_values("name"))

    def test_should_get_dataset(self):

        data = DatasetManager("./tests/resources/local_data")
        df = pd.read_csv("./tests/resources/local_data/train.csv")
        assert_frame_equal(data.get_dataset("local_test"), df)
    
    def test_should_get_dataset_zipped(self):

        data = DatasetManager("./tests/resources/local_data")
        df = pd.read_csv("./tests/resources/local_data/train.csv")
        assert_frame_equal(data.get_dataset("local_zip_test"), df)

    def test_should_get_dataset_unknown_format(self):

        data = DatasetManager("./tests/resources/local_data")
        with self.assertRaises(NotImplementedError):
            data.get_dataset("unknown_test")