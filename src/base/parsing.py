from abc import ABC, abstractmethod
from typing import List, Any, Dict, Union, Generator
import json

import bs4

from decorators import handle_error
from base.items import Category
from exceptions import EmptyPageException


class BaseItemFieldParser(ABC):
    ''' Abstract class for parsing and setting up field '''

    def set_item(self, item: bs4.Tag):
        self.item = item

    @handle_error
    @abstractmethod
    def parse(self) -> str:
        pass

class BaseItemParser(ABC):

    def set_item(self, item: bs4.Tag):
        self.item = item

    def parse_item(self) -> Dict[str, Union[str, int]]:

        item_as_data = {}

        for field_name, field_parser in self.__class__.__dict__.items():
            if isinstance(field_parser, BaseItemFieldParser):
                field_parser.set_item(self.item)
                item_as_data[field_name] = field_parser.parse()              

        return {k:v for k, v in item_as_data.items() if v is not None}

class BaseParser(ABC):

    def __init__(self, item_parser: BaseItemParser) -> None:
        super().__init__()
        self.item_parser = item_parser

    @staticmethod
    @abstractmethod
    def parse_categories(html:str) -> List[Category]:
        pass

    @abstractmethod
    def parse(self, *args, **kwargs) -> Any:
        pass

    def set_data(self, data: Any):
        self.data = data


class BaseHTMLParser(BaseParser):

    @abstractmethod
    def _get_order_list(self):
        pass

    def parse(self) -> Generator[Dict[str, str | int], None, None]:
        
        order_list = self._get_order_list()
        
        if order_list is None or len(order_list) == 0:
            raise EmptyPageException

        for order in order_list:
            self.item_parser.set_item(order)
            parsed_item = self.item_parser.parse_item() 
            yield parsed_item

class BaseJSONParser(BaseParser):
    
    @abstractmethod
    def parse(self, json: Dict[Any, Any]) -> Any:
        pass