from abc import ABC
from typing import List, Type, Optional

from base.items import Category
from base.parsing import (
    BaseParser,
    BaseItemParser
)
from base.scraping import (
    BaseScraper
)
from base.items import (
    Category
)
from base.processing import BaseDataProcessor


class BaseFreelanceService(ABC):
    ''' Base service of freelance exchange '''

    platform: str

    def __init__(self, 
                    data_processor_cls:Type[BaseDataProcessor],
                    scraper_cls:Type[BaseScraper],
                    parser_cls:Type[BaseParser],
                    item_parser_cls:Type[BaseItemParser]):

        item_parser = item_parser_cls()
        parser = parser_cls(item_parser=item_parser)
        self.scraper = scraper_cls(parser=parser)
        self.data_processor = data_processor_cls(scraper=self.scraper)

        self._categories: Optional[List[Category]] = None

    def execute(self, category_names:List[str], count_of_orders:int) -> None:
        data = self.data_processor.get_processed_data(category_names, count_of_orders, self.categories)

        for writing_method in self.writing_methods:
            writing_method(self.platform).write_to_file(data)

        print('Finished')

    def set_writing_methods(self, methods:List):
        self.writing_methods = methods

    @property
    def categories(self) -> List[Category]:
        if self._categories is None:
            self._categories = self.scraper.get_categories()
        return self._categories


    