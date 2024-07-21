from typing import List, Dict, Type

from base.scraping import BaseScraper
from base.items import Category
from base.parsing import BaseParser


class FreelanceRUScraper(BaseScraper):

    base_url: str = "https://www.freelance.ru"
    category_route: str = "/project/search/pro"
