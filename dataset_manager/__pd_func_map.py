from __future__ import unicode_literals

import pandas as pd

PD_FUNC_MAP = {
    "csv":pd.read_csv,
    "xls":pd.read_excel,
    "excel":pd.read_excel,
    "json":pd.read_json
}
