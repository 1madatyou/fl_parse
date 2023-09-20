import multiprocessing
import json
from typing import List, Dict, Type


from base.scraping import BaseScraper
from base.items import Category
from base.parsing import BaseParser

from exceptions import EmptyPageException

from freelance_services.weblancer import URL


class WeblancerScraper(BaseScraper):

    def __init__(self, page_parser: Type[BaseParser]):
        self.page_parser = page_parser

    def get_categories(self) -> List[Category]:
        '''Assigns to class and returns categories'''
        url = URL + '/freelance'
        html_page = self._get_response_text(url)
        categories = self.page_parser.parse_categories(html_page)
        return categories
    
