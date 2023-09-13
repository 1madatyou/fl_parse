
class InvalidStatusCode(Exception):
    
    def __init__(self, *args: object, status_code) -> None:
        self.status_code = status_code
    
    def __str__(self):
        return f'InvalidStatusCode: {self.status_code}'

class EmptyPageException(Exception):
    pass