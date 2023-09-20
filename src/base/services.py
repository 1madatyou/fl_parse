from abc import ABC, abstractmethod

from typing import List
from base.items import Category


class BaseFreelanceService(ABC):
    ''' Base service of freelance exchange '''

    PLATFORM:str = None

    def set_writing_methods(self, methods:List):
        self.writing_methods = methods

    def get_categories(self) -> List[Category]:
        return self.scraper.get_categories()

    