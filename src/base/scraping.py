import requests
from abc import ABC, abstractmethod

from exceptions import InvalidStatusCode


class BaseScraper(ABC):
    '''
    Base class for getting data with http requests
    '''

    @abstractmethod
    def get_categories(self,):
        pass


    @staticmethod
    def _get_response(request_url:str, headers=None) -> requests.Response:
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
        response = BaseScraper._get_response(request_url)
        return response.text