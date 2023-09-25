from abc import ABC, abstractmethod

from typing import List, Type
from base.items import Category
from base.parsing import (
    BaseParser,
    AbstractItemParser
)
from base.scraping import (
    BaseScraper
)
from base.items import (
    Category
)
from base.processing import AbstractDataProcessor

class BaseFreelanceService(ABC):
    ''' Base service of freelance exchange '''

    PLATFORM:str = None

    def __init__(self, 
                    data_processor_cls:Type[AbstractDataProcessor],
                    scraper_cls:Type[BaseScraper],
                    page_parser_cls:Type[BaseParser],
                    item_parser_cls:Type[AbstractItemParser]):

        item_parser = item_parser_cls()
        page_parser = page_parser_cls(item_parser=item_parser)
        self.scraper = scraper_cls(page_parser=page_parser)
        self.data_processor = data_processor_cls(scraper=self.scraper)

        self._categories = None

    def set_writing_methods(self, methods:List):
        self.writing_methods = methods

    @property
    def categories(self) -> List[Category]:
        if self._categories is None:
            self._categories = self.scraper.get_categories()
        return self._categories

    @abstractmethod
    def execute(self, category_names:List[str], count_of_orders:int) -> List:
        pass

    