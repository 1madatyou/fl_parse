import multiprocessing
from abc import ABC, abstractmethod
from typing import List

from base.scraping import BaseScraper
from base.items import Category
from exceptions import EmptyPageException


class BaseDataProcessor(ABC):

    def __init__(self, scraper: BaseScraper):
        self.scraper = scraper

    def get_processed_data(
        self,
        category_names: List[str],
        count_of_orders: int,
        categories: List[Category],
    ) -> List:
        if not isinstance(count_of_orders, int):
            raise TypeError(f"Count of orders must be int, not {type(count_of_orders)}")

        cats_for_parse = [cat for cat in categories if cat.name in category_names]
        pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)
        results = [
            pool.apply_async(self._get_data_by_category, (cat, count_of_orders))
            for cat in cats_for_parse
        ]

        order_list: List = []
        for result in results:
            order_list.extend(result.get())
        return order_list

    def _assemble_url(self, cat: Category, page_num: int) -> str:
        return f"{self.scraper.base_url}{cat.route}?page={page_num}"

    def _get_data_by_category(self, cat: Category, count_of_orders: int) -> List:
        if not isinstance(cat, Category):
            raise TypeError(f"cat must be Category, not {type(cat)}")

        order_list = []
        count_of_orders_left = count_of_orders
        page_num = 1

        while count_of_orders_left > 0:
            href = self._assemble_url(cat, page_num)
            html_page = self.scraper._get_response_text(href)
            parser = self.scraper.parser
            parser.set_data(html_page)
            try:
                for order in parser.parse():
                    order["category"] = cat.name
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
