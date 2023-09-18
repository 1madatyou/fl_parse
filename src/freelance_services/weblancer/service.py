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

from .parsing import (
    WeblancerPageParser,
    WeblancerItemParser
)
from .scraping import (
    WeblancerScraper
)


class WeblancerService(BaseFreelanceService):

    PLATFORM = 'weblancer'

    def __init__(self, 
                    scraper_cls:Type[BaseScraper]=WeblancerScraper,
                    page_parser_cls:Type[BaseParser]=WeblancerPageParser,
                    item_parser_cls:Type[AbstractItemParser]=WeblancerItemParser):

        item_parser = item_parser_cls()
        page_parser = page_parser_cls(item_parser=item_parser)
        self.scraper = scraper_cls(page_parser=page_parser)

        categories = self.scraper.get_categories()

    def get_categories(self) -> List[Category]:
        return self.scraper.get_categories()
    
    def execute(self, category_names:List[str], count_of_orders:int) -> List:
        data = self.scraper.get_processed_data(category_names, count_of_orders)
        print(len(data))
        for writing_method in self.writing_methods:
            writing_method(self.PLATFORM).write_to_file(data)

        

    
    

