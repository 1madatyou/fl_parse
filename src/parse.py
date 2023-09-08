import json
from typing import List
from abc import ABC, abstractmethod

import requests
import bs4

from utils import write_to_file


class BaseParser(ABC):
    ''' Base class for parsers, defines:
    - Data getting method
    - Parsing method
    - Data structuring method 
    '''

    DOMAIN: str = None
    BASE_REQUEST_URL: str = None

    CATEGORIES: dict = None

    def __init__(self, categories: List[str]=None):
        self.categories = categories

    def _get_raw_data(self, request_url: str) -> str:
        headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'}
        response = requests.get(request_url, headers=headers)
        return response.text
        
    def _parse(self, ):
        pass




class WLParser(BaseParser):


    DOMAIN = 'weblancer.net'
    BASE_REQUEST_URL = 'https://www.weblancer.net/freelance/'

    CATEGORIES = {
        'Web programming': 'veb-programmirovanie-31',
        'Application software': 'prikladnoe-po-23'
    }

    def __parse_page(self):
        raw_data = self._get_raw_data('https://www.weblancer.net/freelance/')

        soup_obj = bs4.BeautifulSoup(raw_data, 'html.parser')

        order_table = soup_obj.find('div', {'class': 'cols_table divided_rows'})
        order_items = order_table.findChildren('div', {'class': 'row'})
        # for item in order_items:
        #     ...

    def execute(self):
        write_to_file(self.__parse_page())

WLParser().execute()
            


