from typing import List, Type

from base.parsing import (
    BaseParser,
    AbstractItemParser
)
from base.scraping import (
    BaseScraper
)
from base.services import (
    BaseFreelanceService
)
from base.items import (
    Category
)
from base.processing import AbstractDataProcessor


from .parsing import (
    WeblancerPageParser,
    WeblancerItemParser
)
from .scraping import (
    WeblancerScraper
)
from .processing import WeblancerDataProcessor



class WeblancerService(BaseFreelanceService):

    PLATFORM = 'weblancer'

    def __init__(self, 
                    data_processor_cls:Type[AbstractDataProcessor]=WeblancerDataProcessor,
                    scraper_cls:Type[BaseScraper]=WeblancerScraper,
                    page_parser_cls:Type[BaseParser]=WeblancerPageParser,
                    item_parser_cls:Type[AbstractItemParser]=WeblancerItemParser):

        item_parser = item_parser_cls()
        page_parser = page_parser_cls(item_parser=item_parser)
        self.scraper = scraper_cls(page_parser=page_parser)
        self.data_processor = data_processor_cls(scraper=self.scraper)

        self._categories = None

    @property
    def categories(self) -> List[Category]:
        if self._categories is None:
            self._categories = self.scraper.get_categories()
        return self._categories

    def execute(self, category_names:List[str], count_of_orders:int) -> List:
        data = self.data_processor.get_processed_data(category_names, count_of_orders, self.categories)
        print(len(data))
        for writing_method in self.writing_methods:
            writing_method(self.PLATFORM).write_to_file(data)

        

    
    

