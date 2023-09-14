from abc import ABC, abstractmethod
from typing import List

import requests
import bs4

from exceptions import InvalidStatusCode
from decorators import handle_field_error


class Category:

    def __init__(self, name:str, category_id: int, href:str):
        self.name = name
        self.id = category_id
        self.href = href

    def __str__(self):
        return f'Category: {self.name}'

class AbstractItemField(ABC):
    ''' Abstract class for parsing and setting up field '''

    def set_item(self, item: bs4.Tag):
        self.item = item

    @handle_field_error
    @abstractmethod
    def parse(self) -> str:
        pass

class AbstractItemParser(ABC):

    @abstractmethod
    def parse_item(self):
        pass

class BaseParser:
    pass

class BaseScraper:
    '''
    Base class for getting data with http requests
    '''

    @staticmethod
    def __get_response(request_url:str, headers=None) -> requests.Response:
        if not isinstance(request_url, str):
            raise ValueError(f'Request url must be str, not {type(request_url)}')
        if not headers:
            headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'}
            
        response = requests.get(request_url, headers=headers)
        if response.status_code == 200:
            return response
        else:
            raise InvalidStatusCode

    @staticmethod
    def _get_response_text(request_url: str) -> str:
        response = BaseScraper.__get_response(request_url)
        return response.text
        

class BaseFreelanceService:
    ''' Base service of freelance exchange '''

    @staticmethod
    def show_categories(categories: List[Category]):
        for cat in categories:
            print(f'{cat.id}. {cat.name}')



