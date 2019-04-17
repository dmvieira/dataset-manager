import os
import urllib.request
import zipfile

class DataSource(object):
    def __init__(self, identifier, source, description, format, local_source=None):
        self.source = source
        self.description = description
        format_and_compression = self.__get_formats(format)
        self.format = format_and_compression.get("format")
        self.compression = format_and_compression.get("compression")
        self.local_source = local_source
        self.identifier = identifier

    def is_cached(self):
        local_cache = self.__get_zipped_file_name() if self.is_zipped() else self.local_source
        return self.local_source and os.path.exists(local_cache)

    def download(self):
        if not self.is_cached() :
            download_file_name = self.__get_zipped_file_name() if self.is_zipped() else self.local_source
            urllib.request.urlretrieve(self.source, download_file_name)

    def is_zipped(self):
        return self.compression != None


    def unzip_file(self):
        if self.__is_zipped_and_cached() and self.__zipfile_existis():
            zip_file_name = self.__get_zipped_file_name()
            self.__create_path_to_extract(self.local_source)
            zipfile.ZipFile(zip_file_name).extractall(self.local_source)
            os.remove(zip_file_name)

    def get_file_path_to_read(self):
        files = [self.local_source]
        if self.is_zipped():
            files_local = os.listdir(self.local_source)
            files = [os.path.join(self.local_source, f) for f in files_local]
        return files[0]

    def __get_formats(self, format):
        formats_values = format.split(" ")
        if len(formats_values) == 2:
            return {
                "compression" : formats_values[0],
                "format" : formats_values[1]
            }
        else:
            return {
                "format" : formats_values[0]
            }

    def __get_zipped_file_name(self):
        return "{}.zip".format(self.local_source)

    def __zipfile_existis(self):
        return os.path.exists(self.__get_zipped_file_name())

    def __create_path_to_extract(self, path_to_extract):
        if not os.path.exists(self.local_source):
                os.mkdir(self.local_source)

    def __is_zipped_and_cached(self):
        return self.is_zipped() and self.is_cached()

