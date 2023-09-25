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
                 data_processor_cls: Type[AbstractDataProcessor]=WeblancerDataProcessor, 
                 scraper_cls: Type[BaseScraper]=WeblancerScraper, 
                 page_parser_cls: Type[BaseParser]=WeblancerPageParser, 
                 item_parser_cls: Type[AbstractItemParser]=WeblancerItemParser):
        
        super().__init__(data_processor_cls, scraper_cls, page_parser_cls, item_parser_cls)

    def execute(self, category_names:List[str], count_of_orders:int) -> List:
        data = self.data_processor.get_processed_data(category_names, count_of_orders, self.categories)
        for writing_method in self.writing_methods:
            writing_method(self.PLATFORM).write_to_file(data)

        print('Finished')

        

    
    

