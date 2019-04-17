"""
data_source
module to prepare the datasets
"""
import os
import urllib.request
import zipfile

class DataSource(object):
    """Class to prepare the dataset"""
    def __init__(self, identifier, source, description, read_format, local_source=None):
        self.source = source
        self.description = description
        format_and_compression = self.__get_formats(read_format)
        self.format = format_and_compression.get("format")
        self.compression = format_and_compression.get("compression")
        self.local_source = local_source
        self.identifier = identifier

    def is_cached(self):
        "check if the dataset is cached on local storage"
        local_cache = self.__get_zipped_file_name() if self.is_zipped() else self.local_source
        return self.local_source and os.path.exists(local_cache)

    def download(self):
        "download the dataset from source"
        if not self.is_cached():
            download_file_name = self.local_source
            if self.is_zipped():
                download_file_name = self.__get_zipped_file_name()
            urllib.request.urlretrieve(self.source, download_file_name)

    def is_zipped(self):
        "check if the dataset is zipped"
        return self.compression is not None

    def unzip_file(self):
        "unzip to local_storage and removes the zip file"
        if self.__is_zipped_and_cached() and self.__zipfile_existis():
            zip_file_name = self.__get_zipped_file_name()
            self.__create_path_to_extract()
            zipfile.ZipFile(zip_file_name).extractall(self.local_source)
            os.remove(zip_file_name)

    def get_file_path_to_read(self):
        "get the file path where is the downloaded data"
        files = [self.local_source]
        if self.is_zipped():
            files_local = os.listdir(self.local_source)
            files = [os.path.join(self.local_source, f) for f in files_local]
        return files[0]

    def __get_formats(self, read_format):
        formats_values = read_format.split(" ")
        if len(formats_values) == 2:
            return {
                "compression" : formats_values[0],
                "format" : formats_values[1]
            }
        return {"format" : formats_values[0]}

    def __get_zipped_file_name(self):
        return "{}.zip".format(self.local_source)

    def __zipfile_existis(self):
        return os.path.exists(self.__get_zipped_file_name())

    def __create_path_to_extract(self):
        if not os.path.exists(self.local_source):
            os.mkdir(self.local_source)

    def __is_zipped_and_cached(self):
        return self.is_zipped() and self.is_cached()
