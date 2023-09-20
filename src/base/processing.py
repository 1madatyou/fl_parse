from abc import ABC, abstractmethod
from typing import List


class AbstractDataProcessor(ABC):

    @abstractmethod
    def get_processed_data() -> List:
        pass