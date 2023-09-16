from typing import List, Type

from base.parsing import (
    BaseParser,
    AbstractItemParser
)
from base.scraping import (
    BaseScraper
)
from base.service import (
    BaseFreelanceService
)


from .parsing import (
    WeblancerPageParser,
    WeblancerItemParser
)
from .scraping import (
    WeblancerScraper
)


class WeblancerService(BaseFreelanceService):

    PLATFORM = 'Weblancer'

    def __init__(self, 
                    scraper_cls:Type[BaseScraper]=WeblancerScraper,
                    page_parser_cls:Type[BaseParser]=WeblancerPageParser,
                    item_parser_cls:Type[AbstractItemParser]=WeblancerItemParser):

        item_parser = item_parser_cls()
        page_parser = page_parser_cls(item_parser=item_parser)
        self.scraper = scraper_cls(page_parser=page_parser)

        categories = self.scraper.get_categories()
        
        self.show_categories(categories)
        
        self.category_ids = list(map(int, (input('Введите номера подкатегорий через пробел: ').split(' '))))
        self.count_of_orders = int(input('Введите кол-во заказов: '))
    
    def exec(self) -> List:
        data = self.scraper.get_data(self.category_ids, self.count_of_orders)
        return data

        

    
    

