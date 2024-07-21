from typing import Type

from base.services import BaseFreelanceService

from base.parsing import BaseParser, BaseItemParser
from base.scraping import BaseScraper
from base.services import BaseFreelanceService
from base.processing import BaseDataProcessor
from .parsing import FreelanceRUHTMLParser, FreelanceRUItemParser
from .scraping import FreelanceRUScraper
from .processing import FreelanceRUDataProcessor


class FreelanceRUService(BaseFreelanceService):

    platform = "freelanceRU"

    def __init__(
        self,
        data_processor_cls: Type[BaseDataProcessor] = FreelanceRUDataProcessor,
        scraper_cls: Type[BaseScraper] = FreelanceRUScraper,
        parser_cls: Type[BaseParser] = FreelanceRUHTMLParser,
        item_parser_cls: Type[BaseItemParser] = FreelanceRUItemParser,
    ):

        super().__init__(data_processor_cls, scraper_cls, parser_cls, item_parser_cls)
