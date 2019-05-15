from unittest import TestCase, mock
from dataset_manager.loaders.base import BaseLoader

class TestBaseLoader(TestCase):

    def test_call_csv_method_by_getter(self):
        loader = BaseLoader()
        self.assertEqual(loader.csv, loader["csv"])

    def test_call_xls_method_by_getter(self):
        loader = BaseLoader()
        self.assertEqual(loader.xls, loader["xls"])

    def test_call_xlsx_method_by_getter(self):
        loader = BaseLoader()
        self.assertEqual(loader.xlsx, loader["xlsx"])

    def test_call_json_method_by_getter(self):
        loader = BaseLoader()
        self.assertEqual(loader.json, loader["json"])