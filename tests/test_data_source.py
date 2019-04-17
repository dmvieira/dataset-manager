  
import os
import unittest
from unittest.mock import patch
from dataset_manager.data_source import DataSource

class TestDatasetManager(unittest.TestCase):

    def test_construct_data_source(self):
        test_ds_zip = DataSource("test_id", "/source/to/file", "test dataset", "zip json", "/local/path")

        self.assertEquals("zip",test_ds_zip.compression) 
        self.assertEquals("json",test_ds_zip.format)

        test_ds = DataSource("test_id", "/source/to/file", "test dataset", "json", "/local/path")

        self.assertEquals(None,test_ds.compression) 
        self.assertEquals("json",test_ds.format)

    def test_validate_is_zip(self):
        test_ds_zip = DataSource("test_id", "/source/to/file", "test dataset", "zip json", "/local/path")
        self.assertEquals(True,test_ds_zip.is_zipped()) 
    
        test_ds = DataSource("test_id", "/source/to/file", "test dataset", "json", "/local/path")
        self.assertEquals(False,test_ds.is_zipped()) 

    @patch("os.path.exists")
    def test_validade_zip_cached(self, cache_exists):
        cache_exists.return_value = True
        test_ds = DataSource("test_id", "/source/to/file", "test dataset", "zip json", "/local/path")
        self.assertEquals(True,test_ds.is_cached()) 
        cache_exists.assert_called_with("/local/path.zip")

        cache_exists.return_value = False
        self.assertEquals(False,test_ds.is_cached()) 

    @patch("os.path.exists")
    def test_validade_zip_not_cached(self, cache_exists):
        cache_exists.return_value = False
        test_ds = DataSource("test_id", "/source/to/file", "test dataset", "zip json", "/local/path")
        self.assertEquals(False,test_ds.is_cached()) 
        cache_exists.assert_called_with("/local/path.zip")


    
    @patch("os.path.exists")
    def test_validade_cached(self, cache_exists):
        cache_exists.return_value = True
        test_ds = DataSource("test_id", "/source/to/file", "test dataset", "json", "/local/path")
        self.assertEquals(True,test_ds.is_cached()) 
        cache_exists.assert_called_with("/local/path")

        cache_exists.return_value = False
        self.assertEquals(False,test_ds.is_cached()) 

    @patch("os.path.exists")
    def test_validade_not_cached(self, cache_exists):
        cache_exists.return_value = False
        test_ds = DataSource("test_id", "/source/to/file", "test dataset", "json", "/local/path")
        self.assertEquals(False,test_ds.is_cached()) 
        cache_exists.assert_called_with("/local/path")

    @patch("urllib.request.urlretrieve")
    def test_download(self, download_request):
        test_ds = DataSource("test_id", "/source/to/file", "test dataset", "json", "/local/path")
        test_ds.download()
        download_request.assert_called_with("/source/to/file","/local/path")

    @patch("urllib.request.urlretrieve")
    def test_zip_download(self, download_request):
        test_ds = DataSource("test_id", "/source/to/file", "test dataset", "zip json", "/local/path")
        test_ds.download()
        download_request.assert_called_with("/source/to/file","/local/path.zip")

    @patch("urllib.request.urlretrieve")
    def test_dont_download(self, download_request):
        test_ds = DataSource("test_id", "/source/to/file", "test dataset", "zip json", "/local/path")
        test_ds.is_cached = lambda : True
        test_ds.download()
        download_request.assert_not_called()
