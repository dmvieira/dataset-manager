from __future__ import unicode_literals

from dataset_manager.loaders.base import BaseLoader
import pandas as pd

class PandasLoader(BaseLoader):

    def csv(self, path, *args, **kwargs):
        return pd.read_csv(path, *args, **kwargs)

    def xls(self, path, *args, **kwargs):
        return pd.read_excel(path, *args, **kwargs)

    def xlsx(self, path, *args, **kwargs):
        return pd.read_excel(path, *args, **kwargs)

    def json(self, path, *args, **kwargs):
        return pd.read_json(path, *args, **kwargs)
