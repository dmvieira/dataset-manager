from unittest import TestCase, mock
from dataset_manager.loaders.pandas import PandasLoader

class TestBaseLoader(TestCase):

    @mock.patch("pandas.read_csv")
    def test_call_pandas_csv_method_by_getter(self, mock_read):
        loader = PandasLoader()
        loader["csv"]("file")
        mock_read.assert_called_once_with("file")

    @mock.patch("pandas.read_excel")
    def test_call_pandas_excel_method_by_getter(self, mock_read):
        loader = PandasLoader()
        loader["xls"]("file")
        mock_read.assert_called_once_with("file")

    @mock.patch("pandas.read_excel")
    def test_call_pandas_excelx_method_by_getter(self, mock_read):
        loader = PandasLoader()
        loader["xlsx"]("file")
        mock_read.assert_called_once_with("file")

    @mock.patch("pandas.read_json")
    def test_call_pandas_json_method_by_getter(self, mock_read):
        loader = PandasLoader()
        loader["json"]("file")
        mock_read.assert_called_once_with("file")