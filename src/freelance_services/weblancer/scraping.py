import multiprocessing
import json
from typing import List, Dict


from base import (
    BaseScraper,

    Category
)
from weblancer import URL
from parsing import (
    WeblancerPageParser,
    )


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