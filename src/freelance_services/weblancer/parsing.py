from typing import Dict, Union, List

import bs4

from base.parsing import (
    AbstractItemParser,
    BaseParser
)
from base.fields import AbstractItemField
from base.items import Category

from exceptions import EmptyPageException
from freelance_services.weblancer import URL

class WeblancerItemName(AbstractItemField):

    def parse(self):
        item = self.item
        name = item.find('span', {'class': 'title'}).find('a').text
        return name

class WeblancerItemDescription(AbstractItemField):

    def parse(self):
        item = self.item
        description_paragraphs = item.find('div', {'class': 'text-rich'}).find_all('p')
        description = ' '.join([i.text for i in description_paragraphs])
        return description

class WeblancerItemHref(AbstractItemField):
    
    def parse(self):
        item = self.item
        route = item.find('span', {'class': 'title'}).find('a').get('href')
        url = URL + route
        return url

class WeblancerItemParser(AbstractItemParser):
    '''Class for parsing separated order items from weblancer'''

    name = WeblancerItemName()
    description = WeblancerItemDescription()
    href = WeblancerItemHref()

    def set_item(self, item: bs4.Tag):
        self.item = item
    
    def parse_item(self) -> Dict[str, Union[str, int]]:

        item_as_data = {}

        for field_name, field_parser in self.__class__.__dict__.items():
            print(field_name, field_parser, type(field_parser), isinstance(field_parser, AbstractItemField))
            if isinstance(field_parser, AbstractItemField):
                field_parser.set_item(self.item)
                item_as_data[field_name] = field_parser.parse()              

        return {k:v for k, v in item_as_data.items() if v is not None}

class WeblancerPageParser(BaseParser):
    ''' Class for parsing pages from Weblancer  '''

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