import json
import time

from parsers.weblancer.service import WeblancerService
from utils import time_counter

@time_counter
def main():
    service = WeblancerService()
    data = service.exec()
    
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
    