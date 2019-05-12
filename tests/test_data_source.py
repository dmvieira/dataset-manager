from __future__ import unicode_literals

import unittest
from mock import Mock, patch
from dataset_manager.data_source import DataSource
import dataset_manager
import pandas as pd
from fs.osfs import OSFS
from pandas.testing import assert_frame_equal

class TestDataSource(unittest.TestCase):

    def test_construct_data_source(self):
        test_ds_zip = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", OSFS("/"), local_source = "/local/path")

        self.assertEquals("zip",test_ds_zip.compression) 
        self.assertEquals("json",test_ds_zip.format)

        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "json", OSFS("/"), local_source = "/local/path")

        self.assertEquals(None,test_ds.compression) 
        self.assertEquals("json",test_ds.format)

    def test_validate_is_zip(self):
        test_ds_zip = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", OSFS("/"), local_source = "/local/path")
        self.assertEquals(True,test_ds_zip.is_zipped()) 
    
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "json", OSFS("/"), local_source = "/local/path")
        self.assertEquals(False,test_ds.is_zipped()) 

    def test_validade_zip_cached(self):
        os = Mock()
        os.exists = Mock(return_value= True)
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", os, local_source = "/local/path")
        self.assertTrue(test_ds.is_cached()) 
        os.exists.assert_called_with("/local/path")
        os.exists = Mock(return_value= False)
        self.assertFalse(test_ds.is_cached()) 

    def test_validade_zip_not_cached(self):
        os = Mock()
        os.exists = Mock(return_value= False)
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", os, local_source = "/local/path")
        self.assertFalse(test_ds.is_cached()) 
        os.exists.assert_called_with("/local/path")

    def test_validade_cached(self):
        os = Mock()
        os.exists = Mock(return_value= True)
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "json", os, local_source = "/local/path")
        self.assertTrue(test_ds.is_cached()) 
        os.exists.assert_called_with("/local/path")

        os.exists = Mock(return_value= False)
        self.assertFalse(test_ds.is_cached()) 

    def test_validade_not_cached(self):
        os = Mock()
        os.exists = Mock(return_value= False)
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "json", os, local_source = "/local/path")
        self.assertFalse(test_ds.is_cached()) 
        os.exists.assert_called_with("/local/path")

    def test_download(self):
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "json", OSFS("/"), local_source = "/local/path")
        test_ds._stream_download = Mock()
        test_ds.download()
        test_ds._stream_download.assert_called_with("/local/path")

    def test_zip_download(self):
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", OSFS("/"), local_source = "/local/path")
        test_ds._stream_download = Mock()
        test_ds.download()
        test_ds._stream_download.assert_called_with("/local/path.zip")

    def test_dont_download_if_cached(self):
        test_online_cached = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", OSFS("/"), local_source = "/local/path")
        test_online_cached._stream_download = Mock()
        test_online_cached.is_cached = Mock(return_value=True)
        test_online_cached.download()
        test_online_cached._stream_download.assert_not_called()

    def test_dont_download_if_local(self):
        test_local = DataSource("test_id", "./source/to/file", "test dataset", "zip json", OSFS("/"))
        test_local._stream_download = Mock()
        test_local.download()
        test_local._stream_download.assert_not_called()

    def test_is_onlinde_source(self):
        test_online = DataSource("test_id", "http://source/to/file", "test dataset", "json", OSFS("/"), local_source = "/local/path")
        test_local = DataSource("test_id", "./source/to/file", "test dataset", "json", OSFS("/"))
        self.assertTrue(test_online.is_online_source())
        self.assertFalse(test_local.is_online_source())

    def test_path_to_read_in_dir(self):
        os = Mock()
        os.listdir = Mock(return_value = ["something.json"])
        os.isdir = Mock(return_value = True)

        test_local = DataSource("test_id", "./source/to/file", "test dataset", "json", os)
        test_online = DataSource("test_id", "http://source/to/file", "test dataset", "json", os, local_source = "/local/path")

        expected_local = "./source/to/file/something.json"
        self.assertEqual(expected_local, test_local.get_file_path_to_read())

        expected_online = "/local/path/something.json"
        self.assertEqual(expected_online, test_online.get_file_path_to_read())

    def test_path_to_read_abs(self):
        os = Mock()
        os.listdir = Mock(return_value = ["something.json"])
        os.isdir = Mock(return_value = False)

        test_local = DataSource("test_id", "./source/to/file.json", "test dataset", "json", os)
        test_online = DataSource("test_id", "http://source/to/file", "test dataset", "json", os, local_source = "/local/path.json")

        expected_local = "./source/to/file.json"
        self.assertEqual(expected_local, test_local.get_file_path_to_read())

        expected_online = "/local/path.json"
        self.assertEqual(expected_online, test_online.get_file_path_to_read())

    def test_load_as_pandas_xls(self):
        test_local = DataSource("train", "./tests/resources/local_data/train.csv", "test dataset", "csv", OSFS("/"))
        result = test_local.load_as_pandas()
        expected = pd.DataFrame(
            [["No Name",1],
            ["One Name",0]],
            columns=["name","label"])
        assert_frame_equal(result, expected)

    def test_unzip_local_data(self):
        os = OSFS(".")
        os_remove = os.remove
        os.remove = Mock(return_value = None)
        os.copy("./tests/resources/local_data/base_train.zip", "./tests/resources/local_data/train.zip")
        test_local = DataSource("train", "./tests/resources/local_data/train.zip", "test dataset", "zip csv", os)
        test_local.unzip_file()
        result = os.exists("./tests/resources/local_data/train/train.csv")
        os.remove = os_remove
        os.remove("./tests/resources/local_data/train/train.csv")
        os.remove("./tests/resources/local_data/train.zip")
        os.removedir("./tests/resources/local_data/train")
        self.assertTrue(result)
