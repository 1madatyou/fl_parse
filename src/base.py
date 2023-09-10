from abc import ABC, abstractmethod
from typing import List

import requests

class AbstractItemParser(ABC):

    @abstractmethod
    def parse_item(self):
        pass

class BaseParser(ABC):
    ''' Base class for parsers, defines:
    - Parsing method
    '''

    DOMAIN: str = None
    BASE_REQUEST_URL: str = None

    CATEGORIES: dict = None

    def _get_html(self, request_url: str) -> str:
        headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'}
        response = requests.get(request_url, headers=headers)
        return response.text
    
class Getter:
    
    def _get_html(self, request_url: str) -> str:
        headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'}
        response = requests.get(request_url, headers=headers)
        return response.text

class Structurer:
    pass