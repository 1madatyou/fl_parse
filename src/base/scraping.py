from typing import Type, List
from abc import ABC, abstractmethod

import requests

from exceptions import InvalidStatusCode
from base.parsing import BaseParser
from base.items import Category


class BaseScraper(ABC):
    '''
    Base class for getting data with http requests
    '''

    def __init__(self, page_parser: BaseParser):
        self.page_parser = page_parser

        self._session = None

    def get_categories(self) -> List[Category]:
        '''Returns list of categories'''
        url = self.base_url + self.category_root
        html_page = self._get_response_text(url)
        categories = self.page_parser.parse_categories(html_page)
        return categories

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()
        return self._session

    def _get_response(self, request_url:str, with_session: bool, headers=None, ) -> requests.Response:
        if not isinstance(request_url, str):
            raise ValueError(f'Request url must be str, not {type(request_url)}')
        if not headers:
            headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'}
            

        if with_session:
            response = self.session.get(request_url, headers=headers)
        else:
            response = requests.get(request_url, headers=headers)

        if response.status_code == 200:
            return response
        else:
            raise InvalidStatusCode(response.status_code)

    def _get_response_text(self, request_url: str, with_session=False) -> str:
        response = self._get_response(request_url, with_session)
        return response.text