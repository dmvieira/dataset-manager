import unittest

from dataset_manager.printer import Printer
from dataset_manager import DatasetManager

class TestPrinter(unittest.TestCase):
    def test_should_print_ascii(self):
        self.maxDiff=None
        result = """+---------------------+------------+-----------------------------------------------------------------------------+
|     description     | identifier |                                    source                                   |
+---------------------+------------+-----------------------------------------------------------------------------+
|  my little dataset  |  one_test  | https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv |
| my little dataset 2 |  two_test  | https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv |
+---------------------+------------+-----------------------------------------------------------------------------+"""
        data = DatasetManager("./tests/resources/multiple_data")
        printer = Printer(data.get_datasets())
        self.assertEqual(result, printer.__repr__())

    def test_should_print_html(self):
        self.maxDiff=None
        result = """<table>
    <tr>
        <th>description</th>
        <th>identifier</th>
        <th>source</th>
    </tr>
    <tr>
        <td>my little dataset</td>
        <td>one_test</td>
        <td>https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv</td>
    </tr>
    <tr>
        <td>my little dataset 2</td>
        <td>two_test</td>
        <td>https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv</td>
    </tr>
</table>"""
        data = DatasetManager("./tests/resources/multiple_data")
        printer = Printer(data.get_datasets())
        self.assertEqual(result, printer._repr_html_())
