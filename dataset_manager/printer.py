from prettytable import PrettyTable

class Printer:

    def __init__(self, datasets):
        self._table = PrettyTable()
        self._datasets = datasets
        self._prepare_table()

    def _prepare_table(self):
        fields = set()
        lines = []
        for identifier in sorted(self._datasets.keys()):
            line = dict()
            line["identifier"] = identifier
            line.update(self._datasets[identifier])
            fields |= set(line.keys())
            lines.append(line)
        field_names = sorted(list(fields))
        columns = {}
        for field in field_names:
            for line in lines:
                if not columns.get(field):
                    columns[field] = []
                if line.get(field): 
                    columns[field].append(line[field])
                else:
                    columns[field].append("")
            self._table.add_column(field, columns[field])

    def _repr_html_(self):
        return self._table.get_html_string()

    def __repr__(self):
        return self._table.get_string()