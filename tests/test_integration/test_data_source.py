import unittest
from dataset_manager.data_source import DataSource
from tests.test_integration.test_server import server
from fs.osfs import OSFS


class TestDataSourceIntegration(unittest.TestCase):

    def setUp(self):
        self.server = server()

    def tearDown(self):
        self.server.shutdown()

    def test_should_download_zipped_csv(self):
        os = OSFS("./tests/test_integration/resources/")
        file_name = "test_csv_zipped"
        test_zip_file='http://localhost:8001/local_data/base_train.zip'

        test_ds_zip = DataSource("test_id", test_zip_file, "test dataset", "zip csv", os, local_source = file_name)
        test_ds_zip.download()
        test_ds_zip.unzip_file()
        df = test_ds_zip.load_as_pandas()
        self.assertEqual((2, 2), df.shape)
        os.remove(file_name + "/train.csv")
        os.removedir(file_name)
