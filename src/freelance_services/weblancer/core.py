import multiprocessing
import json
from typing import List, Dict, Union, Type

import bs4
from bs4 import Tag

from base import (
    BaseParser, 
    BaseScraper, 
    AbstractItemParser,

    Category,
)
from exceptions import (
    EmptyPageException
)


DOMAIN = 'weblancer.net'
URL = 'https://www.weblancer.net'

class WeblancerItemParser(AbstractItemParser):
    '''
    Class for parsing separated order items from weblancer
    '''

    def set_item(self, item: Tag):
        self.item = item

    def __get_order_name(self) -> str:
        item = self.item
        try:
            name = item.find('span', {'class': 'title'}).find('a').text
        except Exception:
            name = 'None'
        return name
    
    def __get_order_description(self) -> str:
        item = self.item
        try:
            description_paragraphs = item.find('div', {'class': 'text-rich'}).find_all('p')
            description = ' '.join([i.text for i in description_paragraphs])
        except Exception:
            description = 'None'
        return description
    
    def __get_order_href(self) -> str:
        item = self.item
        try:
            route = item.find('span', {'class': 'title'}).find('a').get('href')
            url = URL + route
            return url
        except Exception:
            return None
    
    def parse_item(self) -> Dict[str, Union[str, int]]:

        item_dict = {
            'name': self.__get_order_name(),
            'description': self.__get_order_description(),
            'href': self.__get_order_href()
        }
        
        return {k:v for k, v in item_dict.items() if v is not None}


class WeblancerPageParser(BaseParser):

    def __init__(self, item_parser=WeblancerItemParser):
        self.item_parser = item_parser

    def set_page(self, html_page: str):
        self.page = html_page

    def parse(self):
        '''Generator which parses the page and yields the data '''
        order_items = self._get_order_items()

        for item in order_items:
            item_parser = self.item_parser
            item_parser.set_item(item)
            parsed_item = item_parser.parse_item()
            yield parsed_item

    def _get_order_items(self):
        soup_obj = bs4.BeautifulSoup(self.page, 'html.parser')
        order_table = soup_obj.find('div', {'class': 'cols_table divided_rows'})
        if order_table:
            order_items = order_table.findChildren('div', {'class': 'row'})
            return order_items
        else:
            raise EmptyPageException
    
    @staticmethod
    def parse_categories(html_page:str) -> List[Category]:
        ''' Parse and returns categories '''

        soup_obj = bs4.BeautifulSoup(html_page, 'html.parser')
        category_tree = soup_obj.find('ul', {'class': 'category_tree'})
        raw_categories = category_tree.find_all('a', {'class': 'dotted'})

        category_list = []
        category_id = 1

        for cat in raw_categories:
            categories = cat.find_next_sibling('ul').find_all('a')
            for subcat in categories:
                category_name = subcat.text.replace('\xa0', ' ')
                category_href = subcat.get('href')
                new_category = Category(category_name, category_id, category_href)
                category_id += 1
                category_list.append(new_category)
        return category_list

            
class WeblancerScraper(BaseScraper):

    def __init__(self, page_parser: WeblancerPageParser):
        self.page_parser = page_parser

    def get_data(self, category_ids:List[int], count_of_orders:int):
        cats_for_parse = [cat for cat in self.categories if cat.id in category_ids]
        order_list = []

        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        results = [pool.apply_async(self._handle_category, (cat, count_of_orders)) for cat in cats_for_parse]

        order_list = [result.get() for result in results]

        with open('result.json', 'w', encoding='utf-8') as file:
            json.dump(order_list, file, ensure_ascii=False)

        return order_list

    def get_categories(self) -> List[Category]:
        '''Receives and returns categories'''
        url = URL + '/freelance'
        html_page = self._get_response_text(url)
        self.categories = self.page_parser.parse_categories(html_page)
        return self.categories
    
    def _handle_category(self, cat:Category, count_of_orders: int) -> Dict[str, List]:
        order_list = []
        orders_left = count_of_orders
        while orders_left > 0:
            page_num = 1
            href = f'{URL}{cat.href}?page={page_num}'
            html_page = self._get_response_text(href)
            parser = self.page_parser
            parser.set_page(html_page)
            for order in parser.parse():
                order_list.append(order)
                orders_left -= 1
                if orders_left == 0:
                    break
        return {cat.name: order_list}

    

                
                

            




      




