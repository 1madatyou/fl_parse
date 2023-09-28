from typing import List

from base.items import Category
from base.processing import BaseDataProcessor
from exceptions import EmptyPageException



class FreelanceRUDataProcessor(BaseDataProcessor):

    def _get_data_by_category(self, cat:Category, count_of_orders: int) -> List:
        order_list = []
        count_of_orders_left = count_of_orders
        page_num = 1

        while count_of_orders_left > 0:
            href = f'{self.scraper.base_url}{cat.href}%3Fpage%3D2&page={page_num}&per-page=25'
            print(href)
            html_page = self.scraper._get_response_text(href, with_session=True)
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