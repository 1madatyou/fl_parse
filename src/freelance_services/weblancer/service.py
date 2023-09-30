from typing import List, Type

from base.parsing import (
    BaseParser,
    BaseItemParser
)
from base.scraping import (
    BaseScraper
)
from base.services import (
    BaseFreelanceService
)
from base.processing import BaseDataProcessor
from .parsing import (
    WeblancerHTMLParser,
    WeblancerItemParser
)
from .scraping import (
    WeblancerScraper
)



class WeblancerService(BaseFreelanceService):

    platform = 'weblancer'

    def __init__(self, 
                 data_processor_cls: Type[BaseDataProcessor]=BaseDataProcessor, 
                 scraper_cls: Type[BaseScraper]=WeblancerScraper, 
                 parser_cls: Type[BaseParser]=WeblancerHTMLParser, 
                 item_parser_cls: Type[BaseItemParser]=WeblancerItemParser):
        
        super().__init__(data_processor_cls, scraper_cls, parser_cls, item_parser_cls)

    

        

    
    

