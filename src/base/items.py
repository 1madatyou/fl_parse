from abc import ABC


class Category:

    def __init__(self, name: str, route: str):
        self.name = name
        self.route = route

    def __str__(self):
        return f"Category: {self.name}"


class AbstractItem(ABC):
    pass
