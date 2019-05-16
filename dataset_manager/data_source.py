"""
data_source
module to prepare the datasets
"""
import os
from urllib import request
from contextlib import closing
import zipfile
import logging
from fs.archive import open_archive
from fs.osfs import OSFS

from dataset_manager.loaders.pandas import PandasLoader

class DataSource(dict):
    """Class to prepare the dataset"""
    def __init__(self, fs, identifier, source, description, format, compression=None, **kwargs):
        self["source"] = self.source = source
        self["description"] = self.description = description
        self.format = format
        if format:
            self["format"] = self.format
        self.compression = compression
        if compression:
            self["compression"] = self.compression
        self.identifier = identifier
        self.extra_args = kwargs
        for key, val in kwargs.items():
            self[key] = val
        self.__fs = fs
        self.__logger = logging.getLogger(self.__class__.__name__)

    def is_cached(self):
        """Check if the dataset is cached on local storage.

        Returns:
            boolean: True, if the dataset is local, otherwise returns False."""
        return self.is_online_source() and self.__fs.exists(self.__get_local_source())

    def is_online_source(self):
        """Check if the source is online or local.
        
        Returns:
            boolean: True, if the source is online, otherwise returns False."""
        return self.source.startswith("http://") or self.source.startswith("https://") or self.source.startswith("ftp://")

    def download(self):
        """Download the dataset from source if the dataset is not cached yet."""
        if not self.is_cached() and self.is_online_source():
            self.__logger.debug("{} is not chached. Downloading ...".format(self.identifier))
            self.__download_to_local()
            self.__logger.debug("{} Downloaded!".format(self.identifier))
        elif self.is_cached():
            self.__logger.debug("{} is cached. Skip Download.".format(self.identifier))
        else:
            self.__logger.debug("{} is not a online source!".format(self.identifier))

    def is_zipped(self):
        """Check if the dataset is zipped

        Returns:
            boolean: True, if the datasource is zipped, otherwise returns False."""
        return self.compression is not None

    def unzip_file(self):
        """Unzip to local_storage and removes the zip file."""
        if self.is_zipped() and self.__zipfile_exists():
            self.__logger.debug("Unzipping {} ...".format(self.identifier))
            zip_file_name = self.__get_zipped_file_name()
            path_to_unzip = self.__get_unzip_folder()
            self.__create_path_to_extract(path_to_unzip)
            with open_archive(self.__fs, zip_file_name) as archive:
                for element in archive.listdir("."):
                    self.__fs.writetext(os.path.join(path_to_unzip, element), archive.readtext(element))
            self.__fs.remove(zip_file_name)
            self.__logger.debug("{} unzipped!".format(self.identifier))
        elif not self.__zipfile_exists():
            self.__logger.debug("local zip file of {} do not existes.")
        else:
            self.__logger.debug("{} is note zipped.")

    def get_file_path_to_read(self):
        """Get the file path where is the downloaded data.

        Returns:
            String: path to file to read. In case of downloadable datasource,
            returns the local storage, otherwise returns the local source."""
        local_source = self.source if not self.is_online_source() else self.__get_local_source()
        files = [local_source]
        if self.__fs.isdir(local_source):
            files_local = self.__fs.listdir(local_source)
            files = [os.path.join(local_source, f) for f in files_local]
        elif zipfile.is_zipfile(local_source):
            files = [local_source.split(".")[0]]
        return files[0]

    def load_as_pandas(self, *args, **kwargs):
        """Uses the field `format` to read the dataset with pandas

        Args:
            *args and **kwargs: extra params passed 
            to pandas read method.

        Returns:
            DataFrame: dataframe with dataset.
        
        Raises:
            NotImplementedError: when __fs is not local filesystem
        """
        if isinstance(self.__fs, OSFS):
            file_to_read = self.get_file_path_to_read()
            loader = PandasLoader()
            read_method = loader[self.format]
            return read_method(os.path.join(self.__fs.root_path, file_to_read), *args, **kwargs)
        else:
            raise NotImplementedError("Pandas only supports OSFS from pyfilesystem2")

    def __get_zipped_file_name(self):
        if not self.is_online_source():
            return self.source
        else:
            return "{}.zip".format(self.__get_local_source()) 

    def __get_unzip_folder(self):
        if self.is_online_source():
            return self.__get_local_source()
        else:
            return os.path.splitext(self.source)[0]

    def __zipfile_exists(self):
        return self.__fs.exists(self.__get_zipped_file_name())


    def __create_path_to_extract(self, path_to_extract):
        if not self.__fs.exists(path_to_extract):
            self.__fs.makedir(path_to_extract)

    def __get_local_source(self):
        local_source = self.extra_args.get("local_source")
        if local_source:
            return local_source
        else:
            raise KeyError("datasource {} must have a 'local_source' field".format(self.identifier))

    def __download_to_local(self):
        download_file_name = self.__get_local_source()
        if self.is_zipped():
            download_file_name = self.__get_zipped_file_name()
        self._download(download_file_name)

    def _download(self, local_filename):
        with closing(request.urlopen(self.source)) as file_stream:
            with self.__fs.open(local_filename, 'wb') as opened_file:
                opened_file.write(file_stream.read())

