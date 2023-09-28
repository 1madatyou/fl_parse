from typing import List, Dict, Type

from base.scraping import BaseScraper
from base.items import Category
from base.parsing import BaseParser


class FreelanceRUScraper(BaseScraper):

    base_url = 'https://www.freelance.ru'
    category_root = '/project/search/pro'


    
