from typing import List

from base.items import Category
from base.processing import BaseDataProcessor
from exceptions import EmptyPageException


class FreelanceRUDataProcessor(BaseDataProcessor):

    def _assemble_url(self, cat: Category, page_num: int):
        return (
            f"{self.scraper.base_url}{cat.route}%3Fpage%3D2&page={page_num}&per-page=25"
        )
