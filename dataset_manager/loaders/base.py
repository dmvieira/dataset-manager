class BaseLoader:

    def __getitem__(self, function):
        for method in dir(self):
            if not method.startswith("_"):
                if method == function:
                    return getattr(self, function)
        raise NotImplementedError

    def csv(self, path, *args, **kwargs):
        raise NotImplementedError

    def xls(self, path, *args, **kwargs):
        raise NotImplementedError

    def xlsx(self, path, *args, **kwargs):
        raise NotImplementedError

    def json(self, path, *args, **kwargs):
        raise NotImplementedError