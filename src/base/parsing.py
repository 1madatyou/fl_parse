from abc import ABC, abstractmethod


class AbstractItemFieldParser(ABC):
    pass

class AbstractItemParser(ABC):

    @abstractmethod
    def parse_item(self):
        pass

class BaseParser:
    pass

class BaseHTMLParser(BaseParser):
    pass

class BaseJSONParser(BaseParser):
    pass