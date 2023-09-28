import bs4

from typing import Any, List, Optional

from base.parsing import BaseHTMLParser, BaseItemParser, BaseItemFieldParser
from base.items import Category

class FreelanceRUItemName(BaseItemFieldParser):
    
    def parse(self):
        name = self.item.find('h2', {'class': 'title'}).get('title')
        return name

class FreelanceRUItemDescription(BaseItemFieldParser):
    
    def parse(self):
        description = self.item.find('a', {'class': 'description'}).text
        return description
    
class FreelanceRUItemHref(BaseItemFieldParser):

    base_url = 'https://freelance.ru'

    def parse(self):
        href = self.base_url + self.item.find('a', {'class': 'description'}).get('href')
        return href

class FreelanceRUItemParser(BaseItemParser):
    
    name = FreelanceRUItemName()
    description = FreelanceRUItemDescription()
    href = FreelanceRUItemHref()


class FreelanceRUHTMLParser(BaseHTMLParser):
    
    def _get_order_list(self) -> Optional[List[bs4.Tag]]:
        soup = bs4.BeautifulSoup(self.page, 'html.parser')
        order_table = soup.find('div', {'id': 'w0'})
        order_list = order_table.find_all('div', {'class': 'project'})
        
        return order_list

    @staticmethod
    def parse_categories(html_page:str) -> List[Category]:
        
        soup = bs4.BeautifulSoup(html_page, 'html.parser')
        category_list = soup.find('div', {'id': 'searchpro-category'})
        category_labels = category_list.find_all('label')

        categories = []

        for label in category_labels:
            site_category_id = label.find('input').get('value')
            category_root = f'/project/search/pro?c=&c%5B%5D={site_category_id}&q=&m=or&e=&a=0&a=1&v=0&v=1&f=&t=&o=0&o=1&b='
            new_category = Category(
                name=label.text,
                href=category_root
            )
            categories.append(new_category)
        
        return categories
            



        

