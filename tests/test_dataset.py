import unittest
from unittest import mock
from fs.osfs import OSFS

from dataset_manager.dataset import DataSet

class TestDataSet(unittest.TestCase):

    def test_construct_dataset(self):
        test_ds_zip = DataSet(OSFS("."), "/local/path", "test_id", "http://source/to/file", "test dataset", "zip")

        self.assertEquals("zip",test_ds_zip.compression) 

        test_ds = DataSet(OSFS("."), "/local/path", "test_id", "http://source/to/file", "test dataset")

        self.assertEquals(None,test_ds.compression) 

    def test_validate_is_zip(self):
        test_ds_zip = DataSet(OSFS("."), "/local/path", "test_id", "http://source/to/file", "test dataset", "zip")
        self.assertEquals(True,test_ds_zip.is_zipped()) 
    
        test_ds = DataSet(OSFS("."), "/local/path", "test_id", "http://source/to/file", "test dataset")
        self.assertEquals(False,test_ds.is_zipped()) 

    def test_validade_zip_cached(self):
        os = mock.Mock()
        os.exists = mock.Mock(return_value= True)
        test_ds = DataSet(os, "/local/path", "test_id", "http://source/to/file", "test dataset", "zip")
        self.assertTrue(test_ds.is_cached()) 
        os.exists.assert_called_with("/local/path")
        os.exists = mock.Mock(return_value= False)
        self.assertFalse(test_ds.is_cached()) 

    def test_validade_zip_not_cached(self):
        os = mock.Mock()
        os.exists = mock.Mock(return_value= False)
        test_ds = DataSet(os, "/local/path", "test_id", "http://source/to/file", "test dataset", "zip")
        self.assertFalse(test_ds.is_cached()) 
        os.exists.assert_called_with("/local/path")

    def test_validade_cached(self):
        os = mock.Mock()
        os.exists = mock.Mock(return_value= True)
        test_ds = DataSet(os, "/local/path", "test_id", "http://source/to/file", "test dataset", "zip")
        self.assertTrue(test_ds.is_cached()) 
        os.exists.assert_called_with("/local/path")

        os.exists = mock.Mock(return_value= False)
        self.assertFalse(test_ds.is_cached()) 

    def test_validade_not_cached(self):
        os = mock.Mock()
        os.exists = mock.Mock(return_value= False)
        test_ds = DataSet(os, "/local/path", "test_id", "http://source/to/file", "test dataset", "zip")
        self.assertFalse(test_ds.is_cached()) 
        os.exists.assert_called_with("/local/path")

    def test_download(self):
        test_ds = DataSet(OSFS("."), "/local/path", "test_id", "http://source/to/file", "test dataset")
        test_ds._download = mock.Mock()
        test_ds.download()
        test_ds._download.assert_called_with("/local/path")

    def test_zip_download(self):
        test_ds = DataSet(OSFS("."), "/local/path", "test_id", "http://source/to/file", "test dataset", "zip")
        test_ds._download = mock.Mock()
        test_ds.download()
        test_ds._download.assert_called_with("/local/path.zip")

    def test_dont_download_if_cached(self):
        test_online_cached = DataSet(OSFS("."), "/local/path", "test_id", "http://source/to/file", "test dataset", "zip")
        test_online_cached._download = mock.Mock()
        test_online_cached.is_cached = mock.Mock(return_value=True)
        test_online_cached.download()
        test_online_cached._download.assert_not_called()

    def test_is_online_source(self):
        test_online = DataSet(OSFS("."), "/local/path", "test_id", "http://source/to/file", "test dataset")
        test_local = DataSet(OSFS("."), "/local/path", "test_id", "./source/to/file", "test dataset")
        self.assertTrue(test_online.is_online_source())
        self.assertFalse(test_local.is_online_source())

    def test_is_ftp_source(self):
        test_online = DataSet(OSFS("."), "/local/path", "test_id", "ftp://source/to/file", "test dataset")
        test_local = DataSet(OSFS("."), "/local/path", "test_id", "./source/to/file", "test dataset")
        self.assertTrue(test_online.is_online_source())
        self.assertFalse(test_local.is_online_source())

    def test_path_to_read_in_dir(self):
        os = mock.Mock()
        os.root_path = "."
        os.listdir = mock.Mock(return_value = ["something.json"])
        os.isdir = mock.Mock(return_value = True)

        test_local = DataSet(os, "/local/path/test_id", "test_id", "./source/to/file", "test dataset")
        test_online = DataSet(os, "/local/path/test_id2", "test_id2", "http://source/to/file", "test dataset")

        expected_local = "././source/to/file/something.json"
        self.assertEqual(expected_local, test_local.uri)

        expected_online = "/local/path/test_id2/something.json"
        self.assertEqual(expected_online, test_online.uri)

    def test_unzip_local_data(self):
        os = OSFS(".")
        os_remove = os.remove
        os.remove = mock.Mock(return_value = None)
        os.copy("./tests/resources/local_data/base_train.zip", "./tests/resources/local_data/train.zip")
        test_local = DataSet(os, "/local/path", "train", "./tests/resources/local_data/train.zip", "test dataset", "zip")
        test_local.unzip_file()
        result = os.exists("./tests/resources/local_data/train/train.csv")
        os.remove = os_remove
        os.remove("./tests/resources/local_data/train/train.csv")
        os.remove("./tests/resources/local_data/train.zip")
        os.removedir("./tests/resources/local_data/train")
        self.assertTrue(result)

    def test_prepare_dataset(self):
        os = mock.Mock()
        test_ds = DataSet(os, "/local/path/test_id2", "test_id2", "http://source/to/file", "test dataset")
        test_ds.download = mock.Mock()
        test_ds.unzip_file = mock.Mock()
        test_ds.prepare()
        test_ds.download.assert_called_once_with()
        test_ds.unzip_file.assert_called_once_with()
