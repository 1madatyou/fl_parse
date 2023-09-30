from typing import List, Optional
from abc import ABC

import requests

from exceptions import InvalidResponse
from base.parsing import BaseParser
from base.items import Category


class BaseScraper(ABC):
    '''
    Base class for getting data with http requests
    '''

    base_url: str
    category_route: str

    def __init__(self, parser: BaseParser):
        self.parser = parser
        
        self._session = None

    def get_categories(self) -> List[Category]:
        '''Returns list of categories'''
        url = self.base_url + self.category_route
        html_page = self._get_response_text(url)
        categories = self.parser.parse_categories(html_page)
        return categories

    @property
    def session(self) -> Optional[requests.Session]:
        if not self._session:
            self._session = requests.Session()
        return self._session

    def _get_response(self, request_url: str, with_session: bool, headers:Optional[dict]=None) -> requests.Response:
        if not isinstance(request_url, str):
            raise TypeError(f'Request url must be str, not {type(request_url)}')
        
        if not headers:
            headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'}
        else:
            if not isinstance(headers, dict): 
                raise TypeError(f'Request url must be str, not {type(request_url)}')

        if with_session:
            response = self.session.get(request_url, headers=headers)
        else:
            response = requests.get(request_url, headers=headers)

        if response.status_code == 200:
            return response
        else:
            raise InvalidResponse(response.status_code)

    def _get_response_text(self, request_url: str, with_session: bool=False) -> str:
        response = self._get_response(request_url, with_session)
        return response.text