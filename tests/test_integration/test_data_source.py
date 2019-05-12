from __future__ import unicode_literals

import unittest
from dataset_manager.data_source import DataSource
from fs.osfs import OSFS

TEST_ZIP_FILE='https://raw.githubusercontent.com/dmvieira/dataset-manager/master/tests/resources/local_data/base_train.zip'

class TestDataSourceIntegration(unittest.TestCase):

    def test_should_download_zipped_csv(self):
        os = OSFS("/")
        file_name = "/tmp/test"

        test_ds_zip = DataSource("test_id", TEST_ZIP_FILE, "test dataset", "zip json", os, local_source = file_name)
        test_ds_zip.download()
        self.assertTrue(os.exists(file_name + ".zip"))
        os.remove(file_name + ".zip")