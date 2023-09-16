from abc import ABC, abstractmethod

import bs4

from decorators import handle_field_error


class AbstractItemField(ABC):
    ''' Abstract class for parsing and setting up field '''

    def set_item(self, item: bs4.Tag):
        self.item = item

    @handle_field_error
    @abstractmethod
    def parse(self) -> str:
        pass