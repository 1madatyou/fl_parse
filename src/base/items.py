from abc import ABC


class Category:

    def __init__(self, name:str, category_id: int, href:str):
        self.name = name
        self.id = category_id
        self.href = href

    def __str__(self):
        return f'Category: {self.name}'
    
class AbstractItem(ABC):
    pass