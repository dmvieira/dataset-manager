import unittest
import pandas as pd
from dataset_manager.dataset import DataSet
from tests.test_integration.test_server import server
from fs.osfs import OSFS


class TestDataSetIntegration(unittest.TestCase):

    def setUp(self):
        self.server = server()

    def tearDown(self):
        self.server.shutdown()

    def test_should_download_zipped_csv(self):
        os = OSFS("./tests/test_integration/resources/")
        file_name = "test_csv_zipped"
        test_zip_file='http://localhost:8001/local_data/base_train.zip'

        test_ds_zip = DataSet(os, file_name, "test_id", test_zip_file, "test dataset", "zip")
        test_ds_zip.download()
        test_ds_zip.unzip_file()
        df = pd.read_csv(test_ds_zip.uri)
        self.assertEqual((2, 2), df.shape)
        os.remove(file_name + "/train.csv")
        os.removedir(file_name)
    
        ## only download
        os = OSFS("./tests/test_integration/resources/")
        file_name = "train.csv"
        test_file='http://localhost:8001/local_data/train.csv'

        test_ds = DataSet(os, file_name, "test_id", test_file, "test dataset")
        test_ds.download()
        test_ds.unzip_file()
        df = pd.read_csv(test_ds.uri)
        self.assertEqual((2, 2), df.shape)
        os.remove(file_name)
