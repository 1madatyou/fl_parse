from typing import Dict, Union, List, Generator, Optional

import bs4

from base.parsing import (
    BaseItemFieldParser,
    BaseItemParser,
    BaseHTMLParser,
)
from base.items import Category

from exceptions import EmptyPageException


class WeblancerItemName(BaseItemFieldParser):

    def parse(self):
        name = self.item.find("span", {"class": "title"}).find("a").text
        return name


class WeblancerItemDescription(BaseItemFieldParser):

    def parse(self):
        description_paragraphs = self.item.find("div", {"class": "text-rich"}).find_all(
            "p"
        )
        description = " ".join([i.text for i in description_paragraphs])
        return description


class WeblancerItemHref(BaseItemFieldParser):

    base_url = "https://weblancer.net"

    def parse(self):
        route = self.item.find("span", {"class": "title"}).find("a").get("href")
        url = self.base_url + route
        return url


class WeblancerItemParser(BaseItemParser):
    """Class for parsing separated order items from weblancer"""

    name = WeblancerItemName()
    description = WeblancerItemDescription()
    href = WeblancerItemHref()


class WeblancerHTMLParser(BaseHTMLParser):
    """Class for parsing pages from Weblancer"""

    def __init__(self, item_parser=WeblancerItemParser):
        self.item_parser = item_parser

    def _get_order_list(self) -> Optional[List[bs4.Tag]]:
        soup_obj = bs4.BeautifulSoup(self.data, "html.parser")
        order_table = soup_obj.find("div", {"class": "cols_table divided_rows"})
        if order_table:
            order_items = order_table.findChildren("div", {"class": "row"})
            return order_items
        else:
            return None

    @staticmethod
    def parse_categories(html_page: str) -> List[Category]:
        """Parse and returns categories"""

        soup_obj = bs4.BeautifulSoup(html_page, "html.parser")
        category_tree = soup_obj.find("ul", {"class": "category_tree"})
        raw_categories = category_tree.find_all("a", {"class": "dotted"})

        category_list = []

        for cat in raw_categories:
            categories = cat.find_next_sibling("ul").find_all("a")
            for subcat in categories:
                category_name = subcat.text.replace("\xa0", " ")
                category_route = subcat.get("href")
                new_category = Category(category_name, category_href)
                category_list.append(new_category)
        return category_list
