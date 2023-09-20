import multiprocessing
from typing import List, Type

from base.processing import AbstractDataProcessor
from base.items import Category
from base.scraping import BaseScraper
from exceptions import EmptyPageException

from . import URL




class WeblancerDataProcessor(AbstractDataProcessor):

    def __init__(self, scraper:BaseScraper):
        self.scraper = scraper

    def _get_data_by_category(self, cat:Category, count_of_orders: int) -> List:
        order_list = []
        count_of_orders_left = count_of_orders
        page_num = 1

        while count_of_orders_left > 0:
            href = f'{URL}{cat.href}?page={page_num}'
            html_page = self.scraper._get_response_text(href)
            parser = self.scraper.page_parser
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

    def get_processed_data(self, category_names:List[str], count_of_orders:int, categories:List[Category]) -> List:
        cats_for_parse = [cat for cat in categories if cat.name in category_names]
        order_list = []
        pool = multiprocessing.Pool(multiprocessing.cpu_count()*2)
        results = [pool.apply_async(self._get_data_by_category, (cat, count_of_orders)) for cat in cats_for_parse]
        order_list = []
        [order_list.extend(result.get()) for result in results]
        return order_list