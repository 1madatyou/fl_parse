from abc import ABC, abstractmethod
from typing import List

import requests

from exceptions import InvalidStatusCode


class Category:

    def __init__(self, name:str, category_id: int, href:str):
        self.name = name
        self.id = category_id
        self.href = href

    def __str__(self):
        return f'Category: {self.name}'

class AbstractItemParser(ABC):

    @abstractmethod
    def parse_item(self):
        pass

class BaseParser(ABC):
    pass

class BaseScraper(ABC):
    '''
    Class for getting data as html with http requests
    '''

    @staticmethod
    def _get_html(request_url: str) -> str:
        headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'}
        response = requests.get(request_url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise InvalidStatusCode

class BaseService:
    
    def show_categories(self, categories: List[Category]):
        for cat in categories:
            print(f'{cat.id}. {cat.name}')



