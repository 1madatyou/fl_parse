from typing import List
from .fields import Category


class BaseFreelanceService:
    ''' Base service of freelance exchange '''

    @staticmethod
    def show_categories(categories: List[Category]):
        for cat in categories:
            print(f'{cat.id}. {cat.name}')