  
import os
import unittest
from mock import patch
from dataset_manager.data_source import DataSource
import dataset_manager
import pandas as pd
from pandas.testing import assert_frame_equal

dataset_manager.data_source._stream_download = lambda x,y : None
remove_local = os.remove

class TestDatasetManager(unittest.TestCase):

    def test_construct_data_source(self):
        test_ds_zip = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", local_source = "/local/path")

        self.assertEquals("zip",test_ds_zip.compression) 
        self.assertEquals("json",test_ds_zip.format)

        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "json", local_source = "/local/path")

        self.assertEquals(None,test_ds.compression) 
        self.assertEquals("json",test_ds.format)

    def test_validate_is_zip(self):
        test_ds_zip = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", local_source = "/local/path")
        self.assertEquals(True,test_ds_zip.is_zipped()) 
    
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "json", local_source = "/local/path")
        self.assertEquals(False,test_ds.is_zipped()) 

    @patch("os.path.exists")
    def test_validade_zip_cached(self, cache_exists):
        cache_exists.return_value = True
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", local_source = "/local/path")
        self.assertEquals(True,test_ds.is_cached()) 
        cache_exists.assert_called_with("/local/path")

        cache_exists.return_value = False
        self.assertEquals(False,test_ds.is_cached()) 

    @patch("os.path.exists")
    def test_validade_zip_not_cached(self, cache_exists):
        cache_exists.return_value = False
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", local_source = "/local/path")
        self.assertEquals(False,test_ds.is_cached()) 
        cache_exists.assert_called_with("/local/path")


    
    @patch("os.path.exists")
    def test_validade_cached(self, cache_exists):
        cache_exists.return_value = True
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "json", local_source = "/local/path")
        self.assertEquals(True,test_ds.is_cached()) 
        cache_exists.assert_called_with("/local/path")

        cache_exists.return_value = False
        self.assertEquals(False,test_ds.is_cached()) 

    @patch("os.path.exists")
    def test_validade_not_cached(self, cache_exists):
        cache_exists.return_value = False
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "json", local_source = "/local/path")
        self.assertEquals(False,test_ds.is_cached()) 
        cache_exists.assert_called_with("/local/path")

    @patch("dataset_manager.data_source._stream_download")
    def test_download(self, download_request):
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "json",local_source = "/local/path")
        test_ds.download()
        download_request.assert_called_with("http://source/to/file","/local/path")

    @patch("dataset_manager.data_source._stream_download")
    def test_zip_download(self, download_request):
        test_ds = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", local_source = "/local/path")
        test_ds.download()
        download_request.assert_called_with("http://source/to/file","/local/path.zip")

    @patch("dataset_manager.data_source._stream_download")
    def test_dont_download_if_cached(self, download_request):
        test_online_cached = DataSource("test_id", "http://source/to/file", "test dataset", "zip json", local_source = "/local/path")
        test_online_cached.is_cached = lambda : True
        test_online_cached.download()

    @patch("dataset_manager.data_source._stream_download")
    def test_dont_download_if_local(self, download_request):
        test_local = DataSource("test_id", "./source/to/file", "test dataset", "zip json")
        test_local.download()
        download_request.assert_not_called()


    def test_is_onlinde_source(self):
        test_online = DataSource("test_id", "http://source/to/file", "test dataset", "json", local_source = "/local/path")
        test_local = DataSource("test_id", "./source/to/file", "test dataset", "json")
        self.assertTrue(test_online.is_online_source())
        self.assertFalse(test_local.is_online_source())

    @patch("os.listdir")
    @patch("os.path.isdir")
    def test_path_to_read_in_dir(self,path_is_dir,ls_in_path):
        path_is_dir.return_value = True
        ls_in_path.return_value = ["something.json"]
        test_local = DataSource("test_id", "./source/to/file", "test dataset", "json")
        test_online = DataSource("test_id", "http://source/to/file", "test dataset", "json", local_source = "/local/path")

        expected_local = "./source/to/file/something.json"
        self.assertEqual(expected_local, test_local.get_file_path_to_read())

        expected_online = "/local/path/something.json"
        self.assertEqual(expected_online, test_online.get_file_path_to_read())

    @patch("os.listdir")
    @patch("os.path.isdir")
    def test_path_to_read_abs(self,path_is_dir,ls_in_path):
        path_is_dir.return_value = False
        ls_in_path.return_value = ["something.json"]
        test_local = DataSource("test_id", "./source/to/file.json", "test dataset", "json")
        test_online = DataSource("test_id", "http://source/to/file", "test dataset", "json", local_source = "/local/path.json")

        expected_local = "./source/to/file.json"
        self.assertEqual(expected_local, test_local.get_file_path_to_read())

        expected_online = "/local/path.json"
        self.assertEqual(expected_online, test_online.get_file_path_to_read())

    def test_load_as_pandas_xls(self):
        test_local = DataSource("train", "./tests/resources/local_data/train.csv", "test dataset", "csv")
        result = test_local.load_as_pandas()
        expected = pd.DataFrame(
            [["No Name",1],
            ["One Name",0]],
            columns=["name","label"])
        assert_frame_equal(result,expected)

    @patch("os.remove")
    def test_unzip_local_data(self,remove):
        remove.return_value = None
        test_local = DataSource("train", "./tests/resources/local_data/train.zip", "test dataset", "zip csv")
        test_local.unzip_file()
        self.assertTrue(os.path.exists("./tests/resources/local_data/train/train.csv"))
        remove_local("./tests/resources/local_data/train/train.csv")
        os.rmdir("./tests/resources/local_data/train")

