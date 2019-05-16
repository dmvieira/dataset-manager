from dataset_manager.loaders.base import BaseLoader

class DaskLoader(BaseLoader):

    def csv(self, path, *args, **kwargs):
        raise NotImplementedError

    def xls(self, path, *args, **kwargs):
        raise NotImplementedError

    def xlsx(self, path, *args, **kwargs):
        raise NotImplementedError

    def json(self, path, *args, **kwargs):
        raise NotImplementedError
