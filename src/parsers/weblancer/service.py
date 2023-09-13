from typing import List

from base import (
    BaseService,
)

from parsers.weblancer.core import (
    WeblancerScraper,
)


class WeblancerService(BaseService):

    def __init__(self, scraper=WeblancerScraper):
        self.scraper = scraper()
        categories = self.scraper.get_categories()
        
        self.show_categories(categories)
        
        self.category_ids = list(map(int, (input('Введите номера подкатегорий через пробел: ').split(' '))))
        self.count_of_orders = int(input('Введите кол-во заказов: '))

    def exec(self):
        data = self.scraper.get_data(self.category_ids, self.count_of_orders)
        return data
        
        

    
    

