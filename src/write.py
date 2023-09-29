import json
from abc import ABC, abstractmethod, abstractproperty
from typing import List, Dict

import pandas


class AbstractDataWriter(ABC):

    EXTENSION: str

    def __init__(self, filename) -> None:
        self.filename = filename

    @property
    def full_file_name(self):
        return f'{self.filename}{self.EXTENSION}'

    @abstractmethod
    def write_to_file(self, data) -> None:
        pass

class JsonWriter(AbstractDataWriter):

    EXTENSION = '.json'

    def write_to_file(self, data):
        with open(self.full_file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

class XLSXWriter(AbstractDataWriter):

    EXTENSION = '.xlsx'

    def _prepare_data(self, data: List[Dict]) -> Dict[str,List]:
        data_structured: Dict = {}
        for item_dict in data:
            for k, v in item_dict.items():
                if data_structured.get(k):
                    data_structured[k].append(v)
                else:
                    data_structured[k] = [v]
        return data_structured

    def write_to_file(self, data: List[Dict]):
        df = pandas.DataFrame(self._prepare_data(data))
        writer = pandas.ExcelWriter(self.full_file_name, engine='xlsxwriter')
        df.to_excel(writer, sheet_name=self.filename, index=False, na_rep='NaN')

        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets[self.filename].set_column(col_idx, col_idx, column_length)
        writer.close()


        


