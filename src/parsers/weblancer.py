import json
from typing import List

import requests
import bs4
from bs4 import Tag

from utils import write_to_file
from base import BaseParser, AbstractItemParser

class BaseWebLancerItemParser(AbstractItemParser):
    '''
    Class for parsing separated order items
    '''

    def __init__(self, item: Tag) -> None:
        self.item = item

    def __get_order_name(self) -> str:
        item = self.item
        name = item.find('span', {'class': 'title'}).find('a').text
        return name
    
    def __get_order_description(self) -> str:
        item = self.item
        description = item.find('div', {'class': 'text-rich'}).find('p').text
        return description
    
    def __get_order_href(self) -> str:
        item = self.item
        route = item.find('span', {'class': 'title'}).find('a').get('href')
        url = WebLancerParser.URL + route
        return url
    
    # def __get_order_id(self) -> str:
    #     item = self.item
    
    def __form_item_data(self) -> dict:
        item_dict = {
            'name': self.item_name,
            'description': self.item_description,
            'href': self.item_href
        }
        item_dict_cleaned = {k:v for k, v in item_dict.items() if v is not None}
        return item_dict_cleaned
    
    def parse_item(self):
        self.item_name = self.__get_order_name()
        self.item_description = self.__get_order_description()
        self.item_href = self.__get_order_href()
        
        item_data = self.__form_item_data()
        
        return item_data

class WebLancerParser(BaseParser):

    DOMAIN = 'weblancer.net'
    URL = 'https://www.weblancer.net'

    CATEGORIES = {
        'Web programming': 'veb-programmirovanie-31',
        'Application software': 'prikladnoe-po-23'
    }

    def __init__(self, item_parser=BaseWebLancerItemParser):
        self.item_parser = item_parser

    def __parse_page(self, url: str):
        raw_data = self._get_html(url)

        soup_obj = bs4.BeautifulSoup(raw_data, 'html.parser')

        order_table = soup_obj.find('div', {'class': 'cols_table divided_rows'})
        order_items = order_table.findChildren('div', {'class': 'row'})

        for item in order_items:
            data = self.item_parser(item).parse_item()

    def execute(self):
        self.__parse_page('https://www.weblancer.net/freelance/')


# class WebLancerUserInputHandler:
    
#     def __init__(self, categories, count_of_orders) -> None:
#         self.categories = categories
#         self.count_of_orders = count_of_orders


