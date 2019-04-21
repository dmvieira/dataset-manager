"""
data_source
module to prepare the datasets
"""
import os
import requests
import zipfile
import logging
from dataset_manager.__pd_func_map import PD_FUNC_MAP

def _stream_download(url,local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk:
                    f.write(chunk)

class DataSource(object):
    """Class to prepare the dataset"""
    def __init__(self, identifier, source, description, read_format, **kwargs):
        self.source = source
        self.description = description
        format_and_compression = self.__get_formats(read_format)
        self.format = format_and_compression.get("format")
        self.compression = format_and_compression.get("compression")
        self.identifier = identifier
        self.extra_args = kwargs
        self.__logger = logging.getLogger(self.__class__.__name__)

    def is_cached(self):
        """Check if the dataset is cached on local storage.

        Returns:
            boolean: True, if the dataset is local, otherwise returns False."""
        return self.is_online_source() and os.path.exists(self.__get_local_source())

    def is_online_source(self):
        """Check if the source is online or local.
        
        Returns:
            boolean: True, if the source is online, otherwise returns False."""
        return self.source.startswith("http://") or self.source.startswith("https://") 

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
        if self.is_zipped() and self.__zipfile_existis():
            self.__logger.debug("Unzipping {} ...".format(self.identifier))
            zip_file_name = self.__get_zipped_file_name()
            local_source = self.__create_path_to_extract()
            zipfile.ZipFile(zip_file_name).extractall(local_source)
            os.remove(zip_file_name)
            self.__logger.debug("{} unzipped!".format(self.identifier))

    def get_file_path_to_read(self):
        """Get the file path where is the downloaded data.

        Returns:
            String: path to file to read. In case of downloadable datasource,
            returns the local storage, otherwise returns the local source."""
        local_source = self.source if not self.is_online_source() else self.__get_local_source()
        files = [local_source]
        if os.path.isdir(local_source):
            files_local = os.listdir(local_source)
            files = [os.path.join(local_source, f) for f in files_local]
        return files[0]

    def load_as_pandas(self, *args, **kwargs):
        """Uses the field `format` to read the dataset with pandas

        Args:
            *args and **kwargs: extra params passed 
            to pandas read method.

        Returns:
            DataFrame: dataframe with dataset.
        """
        file_to_read = self.get_file_path_to_read()
        read_method = PD_FUNC_MAP[self.format]
        return read_method(file_to_read, *args, **kwargs)

    def __get_formats(self, read_format):
        formats_values = read_format.split(" ")
        if len(formats_values) == 2:
            return {
                "compression" : formats_values[0],
                "format" : formats_values[1]
            }
        return {"format" : formats_values[0]}

    def __get_zipped_file_name(self):
        local_path = self.source if not self.is_online_source() else "{}.zip".format(self.__get_local_source()) 
        return local_path

    def __zipfile_existis(self):
        return os.path.exists(self.__get_zipped_file_name())

    def __create_path_to_extract(self):
        local_source = self.__get_local_source()
        if not os.path.exists(local_source):
            os.mkdir(local_source)
        return local_source

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
        _stream_download(self.source, download_file_name)

