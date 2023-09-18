import multiprocessing
import json
from typing import List, Dict, Type


from base.scraping import BaseScraper
from base.items import Category
from base.parsing import BaseParser

from exceptions import EmptyPageException

from freelance_services.weblancer import URL


class WeblancerScraper(BaseScraper):

    def __init__(self, page_parser: Type[BaseParser]):
        self.page_parser = page_parser

    def get_processed_data(self, category_names:List[str], count_of_orders:int):
        cats_for_parse = [cat for cat in self.categories if cat.name in category_names]
        order_list = []
        pool = multiprocessing.Pool(multiprocessing.cpu_count()*2)
        results = [pool.apply_async(self._get_data_by_category, (cat, count_of_orders)) for cat in cats_for_parse]
        order_list = []
        [order_list.extend(result.get()) for result in results]
        return order_list

    def get_categories(self) -> List[Category]:
        '''Assigns to class and returns categories'''
        url = URL + '/freelance'
        html_page = self._get_response_text(url)
        self.categories = self.page_parser.parse_categories(html_page)
        return self.categories
    
    def _get_data_by_category(self, cat:Category, count_of_orders: int) -> List:
        order_list = []
        count_of_orders_left = count_of_orders
        page_num = 1

        while count_of_orders_left > 0:
            href = f'{URL}{cat.href}?page={page_num}'
            html_page = self._get_response_text(href)
            parser = self.page_parser
            parser.set_page(html_page)
            try:
                for order in parser.parse():
                    order['category'] = cat.name
                    order_list.append(order)
                    count_of_orders_left -= 1
                    if count_of_orders_left == 0:
                        break
            except EmptyPageException:
                break
            page_num += 1

        count_of_orders_received = count_of_orders - count_of_orders_left
        print(f'Total {count_of_orders_received} orders by category "{cat.name}"') 
        return order_list